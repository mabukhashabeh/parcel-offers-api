from django_filters import rest_framework as filters

from api.offer.models import Offer


class OfferFilter(filters.FilterSet):
    broker = filters.NumberFilter(field_name='broker__id')
    parcel = filters.UUIDFilter(field_name='parcel__id')

    class Meta:
        model = Offer
        fields = ['broker', 'parcel']