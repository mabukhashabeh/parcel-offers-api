from django.urls import include, path

path('v1/', include([
    path('broker/', include('api.broker.urls')),
    path('offers/', include('api.offer.urls')),
])),