from rest_framework import serializers

#Serializer is a class that converts model to JSON

# ProductSerializer is a class that converts Product model to JSON
class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)