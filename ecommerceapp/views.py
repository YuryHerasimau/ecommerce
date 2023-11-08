from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg

from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response

from .models import Address, Contact, Product, Employee, Supplier, Network
from .serializers import NetworkSerializer, NetworkCreateSerializer, NetworkUpdateSerializer, NetworkDebtStatisticsSerializer
from .permissions import IsActiveEmployeePermission


class NetworkViewSet(viewsets.ModelViewSet):
    queryset = Network.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
        IsActiveEmployeePermission
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('product__id', 'contact__address__country',)


    def get_serializer_class(self):
        if self.action == 'create':
            return NetworkCreateSerializer
        elif self.action == 'update':
            return NetworkUpdateSerializer
        return NetworkSerializer


class NetworkAvgDebtStatisticsAPIView(generics.ListAPIView):
    
    def get(self, request):
        permission_classes = [
            permissions.IsAuthenticated,
            IsActiveEmployeePermission
        ]
        average_debt = Network.objects.aggregate(Avg('debt'))['debt__avg']
        networks_with_high_debt = Network.objects.filter(debt__gt=average_debt)

        response_data = {
            'average_debt': average_debt,
            'networks_with_high_debt': networks_with_high_debt.count(),
        }

        return Response(response_data)