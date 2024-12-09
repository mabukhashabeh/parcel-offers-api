from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ..authentication import JWTAuthentication
from ..pagination import LimitOffsetPagination
from .filters import OfferFilter
from .models import Offer
from .serializers import OfferSerializer


class OfferViewSet(ModelViewSet):
    """
    A viewset for retrieving, creating, updating and deleting offers.
    HTTP Methods: GET, POST, PATCH, DELETE
    Endpoints:
    - /offer/
    - /offer/<id>/
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfferFilter
    ordering = ["-creation_date"]
    http_method_names = ["get", "post", "patch", "delete"]
    pagination_class = LimitOffsetPagination
