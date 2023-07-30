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
@api_view(['GET', 'POST'])
def product_list(request):
    # Check if the request is GET or POST
    if request.method == 'GET':
        # get all products from database
        queryset = Product.objects.select_related('collection').all()
        # convert products to JSON
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        # return JSON
        return Response(serializer.data)

    elif request.method == 'POST':
        # create an object of ProductSerializer
        serializer = ProductSerializer(data=request.data)
        # check if data sent is valid and send validation error if not
        # Manual Method
        # if serializer.is_valid():
        #     serializer.validated_data
        #     return Response('ok')
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Automatic Method
        serializer.is_valid(raise_exception=True)
        serializer.validated_data
        return Response('ok')

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

@api_view()
def collection_detail(request, pk):
    return Response('ok')