from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    """
    Custom pagination class to standardize page size and allow client overrides.
    """
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100