from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
# from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework import status

from .pagination import DefaultPagination
from .filters import ProductFilter
from .models import Cart, CartItem, Customer, OrderItem, Product, Collection, Review
from .serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer, CustomerSerializer, ProductSerializer, CollectionSerializer, ReviewSerializer, UpdateCartItemSerializer

# default django built in response
# def product_list(request):
#     return HttpResponse('OK')

# Implementation using viewsets


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # Use filter backend to filter data
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_class is used to specify which filter to use
    filterset_class = ProductFilter
    # pagination_class is used to specify which pagination to use, but it can be defined in settings for all views
    pagination_class = DefaultPagination
    # search_fields is used to specify which fields to search
    search_fields = ['title', 'description']
    # ordering_fields is used to specify which fields to order by
    ordering_fields = ['unit_price', 'last_update']

    # Override get_queryset method to filter data
    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id=collection_id)
    #     return queryset

    # override get_serializer_context to specify which context to use

    def get_serializer_context(self):
        return {'request': self.request}

    # Overridde the destroy method to check if product is associated with an order item
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

    # Override built in delete method
    # def delete(self, request, pk):
    #     # get product from database
    #     product = get_object_or_404(Product, pk=pk)
    #     # Check if there is any order item with this product
    #     if product.orderitems.count() > 0:
    #         return Response({'error': 'Product cannot be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

# rest framework response (generic view implementing mixins under the hood)
# class ProductList(ListCreateAPIView):
#     # override queryset to specify which data to return
#     # def get_queryset(self):
#     #     return Product.objects.select_related('collection').all()

#     # override serializer class to specify which serializer to use
#     # def get_serializer_class(self):
#     #     return ProductSerializer

#     # Use built in variable queryset to specify which data to return
#     # queryset = Product.objects.select_related('collection').all()
#     queryset = Product.objects.all()
#     # Use built in variable serializer_class to specify which serializer to use
#     serializer_class = ProductSerializer

#     # override get_serializer_context to specify which context to use
#     def get_serializer_context(self):
#         return {'request': self.request}


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

# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     # override queryset to specify which data to return
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     # for custom lookup field (default is pk)
#     # lookup_field = 'id'

#     # Override built in delete method
#     def delete(self, request, pk):
#         # get product from database
#         product = get_object_or_404(Product, pk=pk)
#         # Check if there is any order item with this product
#         if product.orderitems.count() > 0:
#             return Response({'error': 'Product cannot be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

    # Method to handle get request
    # def get(self, request, id):
    #     product = get_object_or_404(Product, pk=id)
    #     serializer = ProductSerializer(product)
    #     return Response(serializer.data)

    # # Method to handle put request
    # def put(self, request, id):
    #     # get product from database
    #     product = get_object_or_404(Product, pk=id)
    #     # Create an object of ProductSerializer
    #     serializer = ProductSerializer(product, data=request.data)
    #     # Check if data sent is valid and send validation error if not
    #     serializer.is_valid(raise_exception=True)
    #     # Save data to database
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    # # Method to handle delete request
    # def delete(self, request, id):
    #     # get product from database
    #     product = get_object_or_404(Product, pk=id)
    #     # Check if there is any order item with this product
    #     if product.orderitems.count() > 0:
    #         return Response({'error': 'Product cannot be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


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

# Implementation using viewsets
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    # Override built in destroy method
    def destroy(self, request, *args, **kwargs):
        collection = self.get_object()
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Override built in delete method
    # def delete(self, request, pk):
    #     collection = get_object_or_404(Collection, pk=pk)
    #     if collection.products.count() > 0:
    #         return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     collection.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

# Collection List with generic class based view
# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(
#         products_count=Count('products')).all()
#     serializer_class = CollectionSerializer

# # Collection Detail with generic class based view
# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(
#         products_count=Count('products')).all()
#     serializer_class = CollectionSerializer

#     def delete(self, request, pk):
#         collection = get_object_or_404(Collection, pk=pk)
#         if collection.products.count() > 0:
#             return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'PUT', 'DELETE'])
# def collection_detail(request, pk):
#     collection = get_object_or_404(
#         Collection.objects.annotate(
#             products_count=Count('products')), pk=pk)
#     if request.method == 'GET':
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if collection.products.count() > 0:
#             return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class ReviewViewSet(ModelViewSet):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # Override the get_queryset method
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    # Override the get_serializer_context method
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}


class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet,):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer

# Modelviewset for cart items


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')


class CustomerViewSet(CreateModelMixin,
                      UpdateModelMixin,
                      RetrieveModelMixin,
                      GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
