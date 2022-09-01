from django.utils import timezone
from rest_framework import serializers

from ..models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

    def validate(self, attrs):
        all_day = attrs['all_day']
        final_date = attrs['final_date']

        if not all_day and final_date is None:
            raise serializers.ValidationError('Must set final date if the event does not take all day')

        if final_date is not None and final_date < attrs['initial_date']:
            raise serializers.ValidationError('Final date must be after initial date')

        return attrs

    def validate_initial_date(self, value):
        if timezone.now() > value:
            raise serializers.ValidationError('Initial date cannot be a past date')

        return value
