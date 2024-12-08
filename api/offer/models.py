from django.db import models
from django.conf import settings
import uuid


class Offer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    broker = models.ForeignKey("broker.Broker", related_name="offers", on_delete=models.CASCADE)
    parcel = models.ForeignKey("parcel.Parcel", related_name="offers", on_delete=models.CASCADE)
    price_per_meter = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES
    )
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Offer {self.title} by {self.broker.name}"
