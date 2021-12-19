from rest_framework import serializers
from .models import *


class InterestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interests
        fields = ('__all__')

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = '__all__'

class TripsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Trips
        fields = ('__all__')