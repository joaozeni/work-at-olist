import traceback
import datetime
import pytz

from rest_framework import serializers
from call.models import Call


class CallSerializer(serializers.Serializer):
    call_id = serializers.IntegerField(required=True)
    timestamp = serializers.DateTimeField()
    type = serializers.CharField()
    source = serializers.CharField(required=False)
    destination = serializers.CharField(required=False)
    call_cost = serializers.FloatField(required=False)

    def create(self, validated_data):
        processed_data = {}

        if validated_data.get('type').upper() == 'START':
            if not validated_data.get('source') and not validated_data.get('destination'):
                raise serializers.ValidationError('start record must include source and destination')
            processed_data['source'] = validated_data.get('source')
            processed_data['destination'] = validated_data.get('destination')
            processed_data['time_start'] = validated_data.get('timestamp')
        elif validated_data.get('type').upper() == 'END':
            processed_data['time_end'] = validated_data.get('timestamp')

        processed_data['call_cost'] = validated_data.get('call_cost')

        try:
            instance, created = Call.objects.update_or_create(call_id=validated_data.get('call_id'), defaults=processed_data)
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                'Got a `TypeError` when calling `%s.objects.create()`. '
                'This may be because you have a writable field on the '
                'serializer class that is not a valid argument to '
                '`%s.objects.create()`. You may need to make the field '
                'read-only, or override the %s.create() method to handle '
                'this correctly.\nOriginal exception was:\n %s' %
                (
                    Call.__name__,
                    Call.__name__,
                    self.__class__.__name__,
                    tb
                )
            )
            raise TypeError(msg)

        return instance

    def validate_timestamp(self, value):
        try:
            call = Call.objects.get(call_id=self.initial_data['call_id'])
        except:
            return value

        if self.initial_data['type'].upper() == 'START' and call.time_start is not None:
            raise serializers.ValidationError("Start aready inserted for this call_id")
        elif self.initial_data['type'].upper() == 'END' and call.time_end is not None:
            raise serializers.ValidationError("Start aready inserted for this call_id")

        if call.time_end is not None and \
                call.time_end.replace(tzinfo=None) < datetime.datetime.strptime(self.initial_data['timestamp'],
                                                                                "%Y-%m-%d %H:%M:%S"):
            raise serializers.ValidationError("Start time must be lower that end")
        elif call.time_start is not None and \
                call.time_start.replace(tzinfo=None) > datetime.datetime.strptime(self.initial_data['timestamp'],
                                                                                  "%Y-%m-%d %H:%M:%S"):
            raise serializers.ValidationError("End time must be higher that start")

        if self.initial_data.get('call_cost'):
            raise serializers.ValidationError("Call cost is calculated by the system")

        if self.initial_data['type'].upper() == 'START' and call.time_end is not None:
            self.initial_data['call_cost'] = self.calculate_cost(datetime.datetime.strptime(
                self.initial_data['timestamp'], "%Y-%m-%d %H:%M:%S"), call.time_end)
        elif self.initial_data['type'].upper() == 'END' and call.time_start is not None:
            self.initial_data['call_cost'] = self.calculate_cost(call.time_start,
                                                                 datetime.datetime.strptime(
                                                                     self.initial_data['timestamp'],
                                                                     "%Y-%m-%d %H:%M:%S")
                                                                 )

        return value

    def calculate_cost(self, time_start, time_end):
        if (time_start.hour >= 22 and time_start.hour <= 6) and (time_end.hour >= 22 and time_end.hour <= 6):
            return 0.36

        difference = int(abs((time_end.replace(tzinfo=pytz.UTC) - time_start.replace(tzinfo=pytz.UTC))
                             .seconds))
        difference = difference/60
        return ((difference*0.09) + 0.36)
