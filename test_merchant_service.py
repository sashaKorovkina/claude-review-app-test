import unittest
from merchant_service import classify_merchant_risk

class TestMerchantRiskClassification(unittest.TestCase):

    def test_classify_low_risk(self):
        merchant_data = {"name": "Merchant B", "group_id": 2}
        result = classify_merchant_risk(102, merchant_data)
        self.assertEqual(result["risk_level"], "low")

    def test_classify_medium_risk(self):
        merchant_data = {"name": "Merchant A", "group_id": 1}
        result = classify_merchant_risk(101, merchant_data)
        self.assertEqual(result["risk_level"], "medium")

    def test_classify_high_risk(self):
        merchant_data = {"name": "Crypto Merch", "group_id": None}
        result = classify_merchant_risk(103, merchant_data)
        self.assertEqual(result["risk_level"], "high")

if __name__ == '__main__':
    unittest.main()
