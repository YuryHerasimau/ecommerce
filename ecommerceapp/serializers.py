from rest_framework import serializers
from .models import Address, Contact, Product, Employee, Supplier, Network


class NetworkSerializer(serializers.ModelSerializer):

    contact = serializers.SlugRelatedField(queryset=Contact.objects.all(), slug_field='email')
    product = serializers.SlugRelatedField(queryset=Product.objects.all(), many=True, slug_field='name')
    employee = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='name')
    supplier = serializers.SlugRelatedField(queryset=Supplier.objects.all(), slug_field='name')

    class Meta:
        model = Network
        fields = ('id', 'name', 'contact', 'product', 'employee', 'supplier', 'debt', 'created_at')
        read_only_fields = ('debt', )


class NetworkCreateSerializer(NetworkSerializer):

    class Meta:
        model = Network
        fields = ('id', 'name', 'contact', 'product', 'employee', 'supplier', 'debt')


class NetworkUpdateSerializer(NetworkSerializer):
    
    class Meta:
        model = Network
        fields = ('id', 'name', 'contact', 'product', 'employee', 'supplier', 'debt')
        read_only_fields = ('debt', )


class NetworkDebtStatisticsSerializer(NetworkSerializer):

    class Meta:
        model = Network
        fields = ('id', 'name', 'debt')