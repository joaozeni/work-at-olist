from rest_framework import viewsets, mixins

from call.models import Call
from call.serializers import CallSerializer


class CallViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Call.objects.all()
    serializer_class = CallSerializer
