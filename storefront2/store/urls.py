from django.urls import path
# from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

# router = DefaultRouter()
# Use default router from rest_framework_nested instead
router = routers.DefaultRouter()
# When using viewsets, we are not going to explicitly create the URL patterns
# Use routers instead
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)
# Nested router
# Create a nested router for reviews
products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
# Register the review viewset
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

# URLConf
urlpatterns = router.urls  + products_router.urls # This will generate the URL patterns for us

# To also inclue custom URL patterns, we can do the following
# urlpatterns = router.urls + [ Other paths here ]

# urlpatterns = [
#     # path('products/', views.product_list),
#     # path('products/<int:id>/', views.product_detail),
#     # path('collections/', views.collection_list),
#     # path('collections/<int:pk>/', views.collection_detail, name='collection-detail'),
#     # path('products/', views.ProductList.as_view()), # Class based view
#     # path('products/<int:pk>/', views.ProductDetail.as_view()), # Class based view, Generic view always takes pk
#     # path('collections/', views.CollectionList.as_view()), # Class based view
#     # path('collections/<int:pk>/', views.CollectionDetail.as_view()), # Class based view
# ]