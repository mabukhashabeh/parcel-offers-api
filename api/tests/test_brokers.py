from rest_framework import status

from api.broker.models import Broker
from api.tests.base_tests import BaseTestCase


class BrokerTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.broker_data = {
            "name": "Test Broker",
            "type": "personal",
            "phone_number": "123456789",
            "email": "test.broker@example.com",
            "bio": "Experienced broker",
            "address": "Test St, City, Country",
        }
        self.broker = Broker.objects.create(**self.broker_data)

    def test_get_broker_list(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.access_token}")
        response = self.client.get("/api/v1/brokers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("name", response.json()[0])

    def test_get_single_broker(self):
        response = self.client.get(f"/api/v1/brokers/{self.broker.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["name"], self.broker.name)

    def test_create_broker(self):
        new_broker = {
            "name": "Test Broker 2",
            "type": "company",
            "phone_number": "987654321",
            "email": "test.broker2@example.com",
            "bio": "Professional broker",
            "address": "Test St, City, Country 2",
        }
        response = self.client.post("/api/v1/brokers/", new_broker, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Broker.objects.count(), 2)

    def test_invalid_create_broker(self):
        invalid_broker = self.broker_data.copy()
        invalid_broker["email"] = ""  # Empty email
        response = self.client.post("/api/v1/brokers/", invalid_broker, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
