from django.db.models.aggregates import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
# from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework import status
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer

# default django built in response
# def product_list(request):
#     return HttpResponse('OK')

# rest framework response (generic view implementing mixins under the hood)
class ProductList(ListCreateAPIView):


    # override queryset to specify which data to return
    # def get_queryset(self):
    #     return Product.objects.select_related('collection').all()

    # override serializer class to specify which serializer to use
    # def get_serializer_class(self):
    #     return ProductSerializer

    # Use built in variable queryset to specify which data to return
    queryset = Product.objects.select_related('collection').all()
    # Use built in variable serializer_class to specify which serializer to use
    serializer_class = ProductSerializer

    # override get_serializer_context to specify which context to use
    def get_serializer_context(self):
        return {'request': self.request}


# rest framework response (Class based view)
# class ProductList(APIView):
#     # Method to handle get request
#     def get(self, request):
#         # get all products from database
#         queryset = Product.objects.select_related('collection').all()
#         # convert products to JSON
#         serializer = ProductSerializer(queryset, many=True, context={'request': request})
#         # return JSON
#         return Response(serializer.data)

#     # Method to handle post request
#     def post(self, request):
#         # create an object of ProductSerializer
#         serializer = ProductSerializer(data=request.data)
#         # check if data sent is valid and send validation error if not
#         # Manual Method
#         # if serializer.is_valid():
#         #     serializer.validated_data
#         #     return Response('ok')
#         # else:
#         #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         # Automatic Method
#         serializer.is_valid(raise_exception=True)
#         # save data to database
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# rest framework response (Method based view)
# @api_view(['GET', 'POST'])
# def product_list(request):
#     # Check if the request is GET or POST
#     if request.method == 'GET':
#         # get all products from database
#         queryset = Product.objects.select_related('collection').all()
#         # convert products to JSON
#         serializer = ProductSerializer(queryset, many=True, context={'request': request})
#         # return JSON
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         # create an object of ProductSerializer
#         serializer = ProductSerializer(data=request.data)
#         # check if data sent is valid and send validation error if not
#         # Manual Method
#         # if serializer.is_valid():
#         #     serializer.validated_data
#         #     return Response('ok')
#         # else:
#         #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         # Automatic Method
#         serializer.is_valid(raise_exception=True)
#         # save data to database
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductDetail(APIView):
    # Method to handle get request
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    # Method to handle put request
    def put(self, request, id):
        # get product from database
        product = get_object_or_404(Product, pk=id)
        # Create an object of ProductSerializer
        serializer = ProductSerializer(product, data=request.data)
        # Check if data sent is valid and send validation error if not
        serializer.is_valid(raise_exception=True)
        # Save data to database
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    # Method to handle delete request
    def delete(self, request, id):
        # get product from database
        product = get_object_or_404(Product, pk=id)
        # Check if there is any order item with this product
        if product.orderitems.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# def product_detail(request, id):
#     # Implementation with try/except
#     # try:
#     #     # get product from database
#     #     product = Product.objects.get(pk=id)
#     #     # convert product to JSON
#     #     serializer = ProductSerializer(product)
#     #     # return JSON
#     #     return Response(serializer.data)
#     # except Product.DoesNotExist:
#     #     # return 404 if product does not exist
#     #     return Response(status=status.HTTP_404_NOT_FOUND)

#     # Implementation with get_object_or_404
#     product = get_object_or_404(Product, pk=id)
#     if request.method == 'GET':
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
    
#     elif request.method == 'PUT':
#         # Create an object of ProductSerializer
#         serializer = ProductSerializer(product, data=request.data)
#         # Check if data sent is valid and send validation error if not
#         serializer.is_valid(raise_exception=True)
#         # Save data to database
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

#     elif request.method == 'DELETE':
#         # Check if there is any order item with this product
#         if product.orderitems.count() > 0:
#             return Response({'error': 'Product cannot be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# Collection List with generic class based view
class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    

@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(
        Collection.objects.annotate(
            products_count=Count('products')), pk=pk)
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)