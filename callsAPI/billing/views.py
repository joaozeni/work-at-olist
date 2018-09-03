from django_filters import CharFilter, DateTimeFilter
from rest_framework import viewsets, mixins, status
from call.models import Call
from rest_framework.response import Response
from django_filters.rest_framework import FilterSet, filters
from datetime import date


# Create your views here.
class BillingViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Call.objects.all()
    filter_class = BillingFilter

    def get_queryset(self, pk):
        period = self.request.GET.get('period')
        try:
            if period:
                month, year = period.split('/')
                month = int(month)
                year = int(year)
            else:
                today = date.today()
                month = today.month - 1 if today.month != 1 else 12
                year = today.year if month != 1 else today.year - 1
        except:
            return Response('The period should be in the {mm}/{yyyy} format', status=status.HTTP_200_OK)

        print(f'{month}/{year}->{pk}')

        return Call.objects.filter(source=pk).filter(time_start__month=month).filter(time_start__year=year).\
            exclude(time_end__isnull=True)

    def retrieve(self, request, *args, **kwargs):
        q_set = self.get_queryset(kwargs['pk'])
        print(q_set)
        return Response(status=status.HTTP_200_OK)