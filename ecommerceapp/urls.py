from django.urls import path
from rest_framework import routers
from .views import (
    NetworkViewSet,
    ProductViewSet,
    NetworkStatsAPIView,
    GenerateQRAPIView
)


router = routers.DefaultRouter()
router.register(r"networks", NetworkViewSet)
router.register(r"products", ProductViewSet)

urlpatterns = router.urls + [
    path('debt_statistics/', NetworkStatsAPIView.as_view(), name='network-stats'),
    path('networks/<int:pk>/generate-qr/', GenerateQRAPIView.as_view(), name='generate-qr'),
]