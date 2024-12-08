from django.urls import include, path

urlpatterns = [
    path('broker/', include('api.broker.urls')),
    path('offers/', include('api.offer.urls')),
]