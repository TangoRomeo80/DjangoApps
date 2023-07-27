from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer

# default django built in response
# def product_list(request):
#     return HttpResponse('OK')

# rest framework response
@api_view()
def product_list(request):
    # get all products from database
    queryset = Product.objects.all()
    # convert products to JSON
    serializer = ProductSerializer(queryset, many=True)
    # return JSON
    return Response(serializer.data)

@api_view()
def product_detail(request, id):
    # Implementation with try/except
    # try:
    #     # get product from database
    #     product = Product.objects.get(pk=id)
    #     # convert product to JSON
    #     serializer = ProductSerializer(product)
    #     # return JSON
    #     return Response(serializer.data)
    # except Product.DoesNotExist:
    #     # return 404 if product does not exist
    #     return Response(status=status.HTTP_404_NOT_FOUND)

    # Implementation with get_object_or_404
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)