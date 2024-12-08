from django.test import TestCase
from api.parcel.models import Parcel

class ParcelTests(TestCase):
    def setUp(self):
        self.parcel_data = {
            "block_number": "B123",
            "neighbourhood": "Central",
            "subdivision_number": "S1",
            "land_use_group": "Residential",
            "description": "Residential land.",
        }
        self.parcel = Parcel.objects.create(**self.parcel_data)

    def test_create_parcel(self):
        new_parcel_data = {
            "block_number": "B456",
            "neighbourhood": "",
            "subdivision_number": "S2",
            "land_use_group": "Commercial",
            "description": "Prime commercial land.",
        }
        new_parcel = Parcel.objects.create(**new_parcel_data)
        self.assertEqual(Parcel.objects.count(), 2)
        self.assertEqual(new_parcel.block_number, "B456")

    def test_retrieve_parcel(self):
        retrieved_parcel = Parcel.objects.get(id=self.parcel.id)
        self.assertEqual(retrieved_parcel.block_number, self.parcel.block_number)

    def test_update_parcel(self):
        self.parcel.block_number = "B789"
        self.parcel.save()
        updated_parcel = Parcel.objects.get(id=self.parcel.id)
        self.assertEqual(updated_parcel.block_number, "B789")

    def test_delete_parcel(self):
        self.parcel.delete()
        self.assertEqual(Parcel.objects.count(), 0)