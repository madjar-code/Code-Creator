from django.db.models import QuerySet
from rest_framework.generics import GenericAPIView
from common.utils import activate_language_from_request


class MultiLingualView(GenericAPIView):
    model = None

    def get_queryset(self) -> QuerySet:
        queryset: QuerySet = self.model.active_objects.all()
        activate_language_from_request(self.request)
        return queryset
