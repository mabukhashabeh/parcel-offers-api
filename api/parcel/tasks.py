import logging

import requests
from celery import shared_task
from django.db.models import Count, F, Q, Value

from api.parcel.models import Parcel

logger = logging.getLogger(__name__)


@shared_task
def monitor_parcel_offers_task():
    """
    Periodic task to monitor parcels and send notifications when all parcels in
    a combination (block_number + subdivision_number) have active offers.
    """
    parcels_with_active_offers = (
        Parcel.objects.values("block_number", "subdivision_number")
        .annotate(
            total_count=Count("id"),
            active_count=Count("id", filter=Q(offers__isnull=False)),
        )
        .filter(total_count=F("active_count"))
        .annotate(
            message=Value("All parcels in this combination have active offers.")
        ).values("block_number", "subdivision_number", "message")
    )

    if notifications:= list(parcels_with_active_offers):
        send_bulk_notifications(notifications)


def send_bulk_notifications(notifications):
    """
    Send notifications in bulk to an external API.
    """
    url = "https://dummyapi.com/notify"
    try:
        response = requests.post(url, json={"notifications": notifications})
        response.raise_for_status()
        logger.info("Successfully sent notifications for all active parcels.")
    except requests.RequestException as e:
        logger.exception(f"Failed to send bulk notifications: {e}")
