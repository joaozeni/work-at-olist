from rest_framework import viewsets, mixins, status
from call.models import Call
from rest_framework.response import Response

# Create your views here.
class BillingViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Call.objects.all()

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)