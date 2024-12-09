import uuid

from django.db import models


class Parcel(models.Model):
    class LandUseGroup(models.TextChoices):
        AGRICULTURAL = "agricultural", "Agricultural"
        RESIDENTIAL = "residential", "Residential"
        COMMERCIAL = "commercial", "Commercial"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    block_number = models.CharField(max_length=50)
    neighbourhood = models.TextField(blank=True, null=True)
    subdivision_number = models.CharField(max_length=50)
    land_use_group = models.CharField(max_length=20, choices=LandUseGroup.choices)
    description = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Parcel {self.block_number} - {self.subdivision_number}"
