from rest_framework import serializers
from .models import Address, Contact, Product, Employee, Network

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    
    class Meta:
        model = Contact
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class NetworkSerializer(serializers.ModelSerializer):
    contact = ContactSerializer()
    products = ProductSerializer(many=True)
    employees = EmployeeSerializer(many=True, read_only=True)
    supplier = serializers.SlugRelatedField(slug_field='name', read_only=True)
    level = serializers.CharField(source='get_level_display', read_only=True)

    class Meta:
        model = Network
        fields = '__all__'
        read_only_fields = ('debt', 'created_at')

class NetworkCreateSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Product.objects.all()
    )
    
    class Meta:
        model = Network
        fields = '__all__'
        read_only_fields = ('debt', 'created_at')

class NetworkDebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = ('id', 'name', 'debt')
