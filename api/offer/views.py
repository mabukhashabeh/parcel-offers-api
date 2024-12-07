from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Offer
from .serializers import OfferSerializer

class OfferViewSet(ModelViewSet):
    """
    A viewset for retrieving, creating, updating and deleting offers.
    HTTP Methods: GET, POST, PUT, DELETE
    Endpoints:
    - /offer/
    - /offer/<id>/
    """
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'description', 'broker__name']
    filterset_fields = ['broker', 'price_per_meter']
    ordering_fields = ['price_per_meter', 'creation_date']
    ordering = ['creation_date']