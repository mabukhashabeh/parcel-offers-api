from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from api.offer.models import Offer
from api.broker.models import Broker
from api.parcel.models import Parcel


class OfferTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.broker = Broker.objects.create(
            name="Test Broker 1",
            type="personal",
            phone_number="123456789",
            email="test.broker@example.com"
        )
        self.parcel = Parcel.objects.create(
            block_number="B101",
            neighbourhood="Downtown",
            subdivision_number="S1",
            land_use_group="Residential",
            description="Prime residential area with excellent facilities."
        )
        self.offer_data = {
            "title": "Amazing Offer",
            "description": "A great deal for land parcels.",
            "broker_id": self.broker.id,
            "price_per_meter": 100.50,
            "parcel_id": self.parcel.id
        }
        self.offer = Offer.objects.create(**self.offer_data)

    def test_get_offer_list(self):
        response = self.client.get("/api/v1/offers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("title", response.json()[0])

    def test_get_single_offer(self):
        response = self.client.get(f"/api/v1/offers/{self.offer.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["title"], self.offer.title)

    def test_create_offer(self):
        new_offer = {
            "title": "Special Discount Offer",
            "description": "Get land at a discounted price.",
            "price_per_meter": 120.00,
            "broker": self.broker.id,
            "parcel": self.parcel.id
        }
        response = self.client.post("/api/v1/offers/", new_offer, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Offer.objects.count(), 2)

    def test_update_offer(self):
        updated_offer = {
            "title": "Updated Offer",
            "description": "A great deal for land parcels.",
            "price_per_meter": 100.50,
            "broker": self.broker.id,
            "parcel": self.parcel.id
        }
        response = self.client.patch(f"/api/v1/offers/{self.offer.id}/", updated_offer, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["title"], updated_offer["title"])

    def test_delete_offer(self):
        response = self.client.delete(f"/api/v1/offers/{self.offer.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Offer.objects.count(), 0)