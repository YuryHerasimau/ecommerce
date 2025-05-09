from rest_framework import viewsets, generics
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from .models import Network, Product
from .serializers import (
    NetworkSerializer, 
    NetworkCreateSerializer,
    ProductSerializer,
    NetworkDebtSerializer
)
from .permissions import IsActiveEmployeePermission


class NetworkViewSet(viewsets.ModelViewSet):
    permission_classes = [IsActiveEmployeePermission]
    queryset = Network.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['contact__address__country', 'products__id']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return NetworkCreateSerializer
        return NetworkSerializer

class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsActiveEmployeePermission]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class NetworkStatsAPIView(generics.GenericAPIView):
    permission_classes = [IsActiveEmployeePermission]
    
    def get(self, request):
        avg_debt = Network.objects.aggregate(avg=Avg('debt'))['avg']
        networks = Network.objects.filter(debt__gt=avg_debt)
        serializer = NetworkDebtSerializer(networks, many=True)
        
        return Response({
            'average_debt': avg_debt,
            'count': networks.count(),
            'networks': serializer.data
        })