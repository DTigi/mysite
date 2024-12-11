from rest_framework import serializers
from .models import Trip


class TripSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Trip
        fields = '__all__' #('title', 'topic')