from django.urls import path
from .views import (
    ProductListAPIView,
    TagListAPIView,
    LabelListAPIView,
    PromotionTagListAPIView,
    ProductListAllAPIView,
)

urlpatterns = [
    path('api/products/', ProductListAPIView.as_view(), name='product-list'),
    path("api/products/all/",  ProductListAllAPIView.as_view(),  name="product-list-all"),
    path('api/tags/', TagListAPIView.as_view(), name='tag-list'),
    path('api/labels/', LabelListAPIView.as_view(), name='label-list'),
    path('api/promotion-tags/', PromotionTagListAPIView.as_view(), name='promotiontag-list'),
]
