"""Vendor-Managed Inventory (VMI), Consignment Stock Tracking & Auto-Consumption Billing Engine."""

import time
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class ConsignmentBatch(BaseModel):
    batch_id: str
    supplier_id: str
    supplier_name: str
    sku: str
    unit_price: float
    received_quantity: int
    consumed_quantity: int = 0
    inward_date: str


class ConsumptionSettlement(BaseModel):
    settlement_id: str
    supplier_id: str
    supplier_name: str
    sku: str
    consumed_quantity: int
    unit_price: float
    total_payable_amount: float
    erpnext_purchase_invoice_reference: str
    consumed_at: float = Field(default_factory=time.time)


class VendorManagedInventoryEngine:
    """Manages supplier-owned consignment stock stored in-house, creating liabilities only upon consumption."""

    def __init__(self, warehouse_name: str = "Consignment Store - Plant 1"):
        self.warehouse_name = warehouse_name
        self.batches: Dict[str, ConsignmentBatch] = {}
        self.settlements: List[ConsumptionSettlement] = []
        self.min_stock_thresholds: Dict[str, int] = {}  # sku -> threshold

    def set_vmi_replenishment_threshold(self, sku: str, min_threshold: int):
        self.min_stock_thresholds[sku] = min_threshold

    def inward_consignment_stock(
        self,
        supplier_id: str,
        supplier_name: str,
        sku: str,
        quantity: int,
        unit_price: float,
        inward_date: str
    ) -> ConsignmentBatch:
        batch_id = f"VMI-{uuid.uuid4().hex[:8].upper()}"
        batch = ConsignmentBatch(
            batch_id=batch_id,
            supplier_id=supplier_id,
            supplier_name=supplier_name,
            sku=sku,
            unit_price=unit_price,
            received_quantity=quantity,
            consumed_quantity=0,
            inward_date=inward_date
        )
        self.batches[batch_id] = batch
        return batch

    def get_available_consignment_stock(self, sku: str) -> int:
        return sum(b.received_quantity - b.consumed_quantity for b in self.batches.values() if b.sku == sku)

    def record_production_consumption(self, sku: str, consume_qty: int) -> ConsumptionSettlement:
        """Consumes stock via FIFO and creates payable liability in ERPNext accounts."""
        available = self.get_available_consignment_stock(sku)
        if available < consume_qty:
            raise ValueError(f"Insufficient VMI consignment stock for {sku} (Available: {available}, Requested: {consume_qty}).")

        # FIFO allocation across supplier batches
        active_batches = [b for b in self.batches.values() if b.sku == sku and (b.received_quantity - b.consumed_quantity) > 0]
        active_batches.sort(key=lambda x: x.inward_date)

        remaining_to_consume = consume_qty
        total_payable = 0.0
        primary_supplier = active_batches[0].supplier_name
        primary_supp_id = active_batches[0].supplier_id
        unit_price = active_batches[0].unit_price

        for batch in active_batches:
            unconsumed = batch.received_quantity - batch.consumed_quantity
            take = min(unconsumed, remaining_to_consume)
            batch.consumed_quantity += take
            total_payable += take * batch.unit_price
            remaining_to_consume -= take
            if remaining_to_consume == 0:
                break

        settlement_id = f"SETTLE-{uuid.uuid4().hex[:8].upper()}"
        invoice_ref = f"PINV-VMI-{settlement_id[:10]}"

        settlement = ConsumptionSettlement(
            settlement_id=settlement_id,
            supplier_id=primary_supp_id,
            supplier_name=primary_supplier,
            sku=sku,
            consumed_quantity=consume_qty,
            unit_price=unit_price,
            total_payable_amount=round(total_payable, 2),
            erpnext_purchase_invoice_reference=invoice_ref
        )
        self.settlements.append(settlement)
        return settlement

    def check_vendor_replenishment_alerts(self, sku: str) -> Dict[str, Any]:
        """Notifies supplier portal if consignment stock drops below agreed safety buffer."""
        curr = self.get_available_consignment_stock(sku)
        thresh = self.min_stock_thresholds.get(sku, 0)
        needs_replenishment = curr <= thresh

        return {
            "sku": sku,
            "current_consignment_stock": curr,
            "min_threshold": thresh,
            "needs_replenishment": needs_replenishment,
            "suggested_delivery_qty": (thresh * 2) - curr if needs_replenishment else 0
        }
