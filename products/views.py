# products/views.py
from rest_framework import generics
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from django.db.models import Min, Max

from .models import Product, Tag, Label, PromotionTag
from .serializers import (
    ProductSerializer,
    TagSerializer,
    LabelSerializer,
    PromotionTagSerializer,
)

class ProductPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductFilter(filters.FilterSet):
    price_min = filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = {
            'price': ['gte', 'lte'],
            'tags__name': ['exact'],
            'promotion_tags__name': ['exact'],
            'labels__name': ['exact'],
        }

class ProductListAPIView(generics.ListAPIView):
    """GET /api/products/ -> 상품 목록 페이징 + 필터링 + 검색 + 가격 범위"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['product_name', 'product_description']

    def list(self, request, *args, **kwargs):
        # 필터·검색이 적용된 queryset
        qs = self.filter_queryset(self.get_queryset())

        # aggregate로 min/max 계산
        agg = qs.aggregate(
            min_price=Min('price'),
            max_price=Max('price'),
        )

        # 페이징 처리
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'min_price': agg['min_price'] or 0,
                'max_price': agg['max_price'] or 0,
                'results': serializer.data,
            })

        # 페이징 미사용 시
        serializer = self.get_serializer(qs, many=True)
        return Response({
            'min_price': agg['min_price'] or 0,
            'max_price': agg['max_price'] or 0,
            'results': serializer.data,
        })

# 페이지네이션 없이 전체 반환
class ProductListAllAPIView(generics.ListAPIView):
    """GET /api/products/all/  →  필터 적용 후 전체 결과 반환 (무한 스크롤·엑셀 다운로드 등용)"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    pagination_class = None            # ← 반드시 None 지정

# --- Lookup APIs for filter options (전체 조회) ---
class TagListAPIView(generics.ListAPIView):
    """GET /api/tags/ -> 전체 516개 태그 반환 (페이징 비활성화)"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None

class LabelListAPIView(generics.ListAPIView):
    """GET /api/labels/ -> 전체 라벨 반환 (페이징 비활성화)"""
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    pagination_class = None

class PromotionTagListAPIView(generics.ListAPIView):
    """GET /api/promotion-tags/ -> 전체 프로모션 태그 반환 (페이징 비활성화)"""
    queryset = PromotionTag.objects.all()
    serializer_class = PromotionTagSerializer
    pagination_class = None
