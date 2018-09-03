from rest_framework import viewsets, mixins, status

from call.models import Call
from call.serializers import CallSerializer
from rest_framework.response import Response


class CallViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Call.objects.all()
    serializer_class = CallSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.data)
        return Response(status=status.HTTP_201_CREATED)
