from rest_framework import serializers
from .models import NetworkNode, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'model', 'release_date']


class NetworkNodeSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    level = serializers.SerializerMethodField()

    class Meta:
        model = NetworkNode
        fields = [
            'id', 'name', 'email', 'country', 'city',
            'street', 'house_number', 'products', 'supplier',
            'debt', 'created_at', 'level'
        ]
        read_only_fields = ['debt', 'created_at', 'level']

    def get_level(self, obj):
        return obj.level

    def validate_supplier(self, value):
        if self.instance and value == self.instance:
            raise serializers.ValidationError("Cannot be supplier to yourself")
        return value

    def validate(self, data):
        supplier = data.get('supplier')
        if supplier and supplier.level >= 2:
            raise serializers.ValidationError("Supplier level must be less than 2")
        return data

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        node = NetworkNode.objects.create(**validated_data)
        for product_data in products_data:
            product, _ = Product.objects.get_or_create(**product_data)
            node.products.add(product)
        return node

    def update(self, instance, validated_data):
        products_data = validated_data.pop('products', [])
        instance = super().update(instance, validated_data)
        instance.products.clear()
        for product_data in products_data:
            product, _ = Product.objects.get_or_create(**product_data)
            instance.products.add(product)
        return instance
