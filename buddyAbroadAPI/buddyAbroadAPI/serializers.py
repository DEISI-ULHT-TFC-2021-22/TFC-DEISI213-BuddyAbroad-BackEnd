from rest_framework import serializers
from .models import *


class InterestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interests
        fields = [
            'name'
        ]

class UserSerializer(serializers.ModelSerializer):

    interests = InterestsSerializer(
        many = True
    )

    class Meta:
        model = Users
        fields = '__all__'

    def create(self, validated_data):
        interests_data = validated_data.pop('interests')
        user = Users.objects.create(**validated_data)
        for interest_data in interests_data:
            interest_data_obj = Interests.objects.get(name=interest_data['name'])
            user.interests.add(interest_data_obj)

        return user


class TripsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Trips
        fields = ('__all__')