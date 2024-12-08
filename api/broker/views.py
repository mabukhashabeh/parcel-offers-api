from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Broker
from .serializers import BrokerSerializer
from ..pagination import LimitOffsetPagination


class BrokerViewSet(ModelViewSet):
    """
    A viewset for retrieving and creating brokers.
    HTTP Methods: GET, POST
    Endpoints:
    - /broker/
    - /broker/<id>/
    """
    queryset = Broker.objects.all()
    serializer_class = BrokerSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    http_method_names = ['get', 'post']
    search_fields = ['name', 'email']
    filterset_fields = ['type']
    ordering_fields = ['name', 'creation_date']
    ordering = ['creation_date']
    pagination_class = LimitOffsetPagination