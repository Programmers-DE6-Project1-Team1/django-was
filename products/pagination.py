from rest_framework.pagination import PageNumberPagination

class ProductPagination(PageNumberPagination):
    # 쿼리 파라미터로 page_size 조정 허용
    page_size_query_param = 'page_size'
    max_page_size = 24
