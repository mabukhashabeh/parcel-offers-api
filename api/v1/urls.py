from django.urls import include, path

urlpatterns = [
    path("brokers/", include("api.broker.urls")),
    path("offers/", include("api.offer.urls")),
]
