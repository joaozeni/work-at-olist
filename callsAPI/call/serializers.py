import traceback

from rest_framework import serializers
from call.models import Call


class CallSerializer(serializers.Serializer):
    call_id = serializers.IntegerField(required=True)
    timestamp = serializers.DateTimeField()
    type = serializers.CharField()
    source = serializers.CharField()
    destination = serializers.CharField()

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

        return value
