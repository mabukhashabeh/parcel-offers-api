import logging

import requests
from celery import shared_task
from django.db.models import Count, F, Q

from api.parcel.models import Parcel

logger = logging.getLogger(__name__)


@shared_task
def monitor_parcel_offers_task():
    """
    Periodic task to monitor parcels and send notifications when all parcels in
    a combination (block_number + subdivision_number) have active offers.
    """
    parcels = (
        Parcel.objects.values("block_number", "subdivision_number")
        .annotate(
            total_count=Count("id"),
            active_count=Count("id", filter=Q(offers__isnull=False)),
        )
        .filter(total_count=F("active_count"))
    )  # only combinations where all are has active offers

    notifications = [
        {
            "block_number": parcel["block_number"],
            "subdivision_number": parcel["subdivision_number"],
            "message": "All parcels in this combination have active offers.",
        }
        for parcel in parcels
    ]

    if len(notifications) > 0:
        send_bulk_notifications(notifications)  # send bulk dummy notifications


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
