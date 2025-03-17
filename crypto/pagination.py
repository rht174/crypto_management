from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict


class GroupedPricesPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('organizations', data)
        ]))


class NestedPricesPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'prices_per_page'
    max_page_size = 100

    def paginate_prices(self, prices, request):
        self.page_size = int(request.query_params.get(
            self.page_size_query_param, self.page_size))
        paginator = self.django_paginator_class(prices, self.page_size)
        page_number = request.query_params.get('price_page', 1)
        try:
            self.page = paginator.page(page_number)
        except Exception as exc:
            self.page = paginator.page(1)

        return list(self.page)

    def get_prices_pagination_data(self):
        return {
            'count': self.page.paginator.count,
            'next': self.page.has_next(),
            'previous': self.page.has_previous(),
            'current_page': self.page.number,
            'total_pages': self.page.paginator.num_pages
        }
