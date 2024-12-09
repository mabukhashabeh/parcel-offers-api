from django.core.paginator import Paginator
from django.utils.functional import cached_property
from rest_framework.pagination import LimitOffsetPagination as BaseLimitOffsetPagination

DEFAULT_PAGE_SIZE = 10


class CustomPaginator(Paginator):
    @cached_property
    def count(self):
        # only select 'id' for counting, much cheaper
        return self.object_list.values("id").count()


class LimitOffsetPagination(BaseLimitOffsetPagination):
    page_size = DEFAULT_PAGE_SIZE
    django_paginator_class = CustomPaginator

    def get_offset(self, request):
        current_offset = super().get_offset(request)
        if 0 < self.count < current_offset:
            return 0
        return current_offset
