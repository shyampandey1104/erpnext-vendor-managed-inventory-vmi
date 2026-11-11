# ERPNext Vendor-Managed Inventory (VMI) & Consignment Engine 🏭🤝

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![ERPNext](https://img.shields.io/badge/ERPNext-v14%20%7C%20v15-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Build](https://img.shields.io/badge/Build-Passing-brightgreen.svg)

An enterprise Vendor-Managed Inventory (VMI) and supplier consignment stock management engine for **ERPNext Manufacturing & Supply Chain**. Enables companies to hold physical raw materials on site while deferring financial liability until actual manufacturing consumption.

---

## 🚀 Key Features

- **Consignment Stock Custody Accounting**: Tracks supplier-owned physical inventory located in your factory warehouse without creating upfront accounts payable liability.
- **Pay-Upon-Consumption FIFO Trigger**: Automatically spawns ERPNext `Purchase Invoice` debit vouchers only when material is issued to a work order.
- **Supplier Self-Replenishment Telemetry**: Notifies vendor portals with automated refill recommendations when consignment stock breaches agreed safety levels.
- **Multi-Vendor Batch Segregation**: Eliminates ownership ambiguity across overlapping commodity suppliers.

---

## 📦 Installation & Setup

```bash
git clone https://github.com/shyampandey1104/erpnext-vendor-managed-inventory-vmi.git
cd erpnext-vendor-managed-inventory-vmi
pip install -r requirements.txt
```

---

## 🛠️ Usage Example

```python
from vmi.engine import VendorManagedInventoryEngine

engine = VendorManagedInventoryEngine()
engine.set_vmi_replenishment_threshold("STEEL-BAR-10MM", min_threshold=50)

# Supplier inwards 100 bars on consignment
engine.inward_consignment_stock(
    supplier_id="SUPP-JINDAL",
    supplier_name="Jindal Steel & Power",
    sku="STEEL-BAR-10MM",
    quantity=100,
    unit_price=850.0,
    inward_date="2026-08-01"
)

# Workshop consumes 20 bars
bill = engine.record_production_consumption("STEEL-BAR-10MM", consume_qty=20)
print(f"Billed: ₹{bill.total_payable_amount} | Invoice Ref: {bill.erpnext_purchase_invoice_reference}")
```

---

## 🧪 Testing

```bash
pytest tests/
```

---

## 📄 License
MIT License. Created with ❤️ by [Shyam Pandey](https://github.com/shyampandey1104).
