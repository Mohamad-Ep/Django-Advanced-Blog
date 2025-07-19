from rest_framework import pagination
from rest_framework.response import Response
# __________________________________________________________

class CustomPagination(pagination.PageNumberPagination):
    
    # page_size = 5
    # page_size_query_param = 'page_size'
    # max_page_size = 20
    
    page_size = 5
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'number_objects': self.page.paginator.count,
            'number_pages': self.page.paginator.num_pages,
            'results': data
        })
# __________________________________________________________