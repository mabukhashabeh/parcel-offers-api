from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ..authentication import JWTAuthentication
from ..pagination import LimitOffsetPagination
from .models import Broker
from .serializers import BrokerSerializer


class BrokerViewSet(ModelViewSet):
    """
    A viewset for retrieving and creating brokers.
    HTTP Methods: GET, POST
    Endpoints:
    - /broker/
    - /broker/<id>/
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Broker.objects.all()
    serializer_class = BrokerSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    http_method_names = ["get", "post"]
    filterset_fields = ["name", "email", "type"]
    ordering = ["-creation_date"]
    pagination_class = LimitOffsetPagination
