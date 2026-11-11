import unittest
from vmi.engine import VendorManagedInventoryEngine


class TestVendorManagedInventoryEngine(unittest.TestCase):
    def setUp(self):
        self.engine = VendorManagedInventoryEngine()
        self.engine.set_vmi_replenishment_threshold("RAW-STEEL-COIL", min_threshold=10)

    def test_inward_and_consumption_liability(self):
        # Supplier delivers 20 coils on consignment
        b1 = self.engine.inward_consignment_stock(
            supplier_id="SUPP-TATA-STEEL",
            supplier_name="Tata Steel Ltd",
            sku="RAW-STEEL-COIL",
            quantity=20,
            unit_price=45000.0,
            inward_date="2026-07-01"
        )
        self.assertEqual(self.engine.get_available_consignment_stock("RAW-STEEL-COIL"), 20)

        # Factory consumes 5 coils for production
        settlement = self.engine.record_production_consumption("RAW-STEEL-COIL", consume_qty=5)
        self.assertEqual(settlement.consumed_quantity, 5)
        self.assertEqual(settlement.total_payable_amount, 225000.0)  # 5 * 45,000
        self.assertEqual(self.engine.get_available_consignment_stock("RAW-STEEL-COIL"), 15)

    def test_replenishment_alert_triggered(self):
        self.engine.inward_consignment_stock(
            supplier_id="SUPP-TATA-STEEL",
            supplier_name="Tata Steel Ltd",
            sku="RAW-STEEL-COIL",
            quantity=12,
            unit_price=45000.0,
            inward_date="2026-07-01"
        )
        # Consume 5 coils -> remaining 7 (below threshold 10)
        self.engine.record_production_consumption("RAW-STEEL-COIL", 5)
        alert = self.engine.check_vendor_replenishment_alerts("RAW-STEEL-COIL")
        self.assertTrue(alert["needs_replenishment"])
        self.assertEqual(alert["current_consignment_stock"], 7)


if __name__ == "__main__":
    unittest.main()
