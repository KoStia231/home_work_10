from rest_framework.pagination import PageNumberPagination


class MyPageNumberPagination(PageNumberPagination):
    page_size = ...
    page_size_query_param = 'page_size'
    max_page_size = ...
