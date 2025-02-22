from rest_framework.pagination import PageNumberPagination


class MessagePagination(PageNumberPagination):
    """
    Pagination for messages in a conversation.
    """

    page_size = 20  # Default page size
    page_query_param = "PG"
    page_size_query_param = "PGZ"
    max_page_size = 20
