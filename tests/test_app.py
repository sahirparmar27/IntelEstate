import unittest
import app as intel_app

class IntelEstateAppTests(unittest.TestCase):
    def setUp(self):
        intel_app.app.config["TESTING"] = True
        self.client = intel_app.app.test_client()

    def test_home_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"INTEL ESTATE", response.data)

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")

    def test_unknown_location_is_rejected(self):
        response = self.client.post("/predict", data={
            "location": "not-a-real-ahmedabad-location-xyz", "area_type": "super",
            "property_type": "flat", "sqft": "1500", "bhk_type": "3"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Location not found", response.data)

    def test_unrecognized_lookalike_location_is_rejected(self):
        response = self.client.post("/predict", data={
            "location": "dijik astra", "area_type": "built-up",
            "property_type": "flat", "sqft": "1000", "bhk_type": "2"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Location not found", response.data)
        self.assertNotIn(b"ESTIMATED VALUE", response.data)

    def test_random_gibberish_location_is_rejected(self):
        response = self.client.post("/predict", data={
            "location": "asdfghjk", "area_type": "carpet",
            "property_type": "flat", "sqft": "1300", "bhk_type": "2"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Invalid location", response.data)
        self.assertNotIn(b"ESTIMATED VALUE", response.data)

    def test_invalid_area_is_rejected(self):
        response = self.client.post("/predict", data={
            "location": "satellite", "area_type": "super",
            "property_type": "flat", "sqft": "10", "bhk_type": "3"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Area must be between", response.data)

    def test_valid_prediction(self):
        response = self.client.post("/predict", data={
            "location": "satellite", "area_type": "super",
            "property_type": "flat", "sqft": "1500", "bhk_type": "3"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Indicative model estimate", response.data)
        self.assertIn(b"Matched location", response.data)

if __name__ == "__main__":
    unittest.main()
