from rest_framework import serializers
from call.models import Call


class CallSerializer(serializers.ModelSerializer):

    class Meta:
        model = Call
        fields = ['call_id', 'time_start', 'time_end', 'source', 'destination']
