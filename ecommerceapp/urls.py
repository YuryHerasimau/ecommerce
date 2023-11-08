from django.urls import path
from rest_framework import routers
from .views import NetworkViewSet, NetworkAvgDebtStatisticsAPIView


router = routers.DefaultRouter()
router.register('api/network', NetworkViewSet, 'network')

urlpatterns = router.urls + [
    path('debt_statistics/', NetworkAvgDebtStatisticsAPIView.as_view(), name='avg-debt'),
]