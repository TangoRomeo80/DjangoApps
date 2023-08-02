from django.urls import path
from . import views

# URLConf
urlpatterns = [
    # path('products/', views.product_list),
    # path('products/<int:id>/', views.product_detail),
    # path('collections/', views.collection_list),
    # path('collections/<int:pk>/', views.collection_detail, name='collection-detail'),
    path('products/', views.ProductList.as_view()), # Class based view
    path('products/<int:id>/', views.ProductDetail.as_view()), # Class based view
]