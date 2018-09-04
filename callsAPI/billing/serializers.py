import pytz

from rest_framework import serializers
from call.models import Call


class BillingSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()

    def get_duration(self, obj):
        seconds_passed = int(abs((obj.time_end.replace(tzinfo=pytz.UTC) - obj.time_start.replace(tzinfo=pytz.UTC)).
                                 seconds))
        return seconds_passed

    class Meta:
        model = Call
        fields = ['call_id', 'time_start', 'time_end', 'destination', 'call_cost', 'duration']