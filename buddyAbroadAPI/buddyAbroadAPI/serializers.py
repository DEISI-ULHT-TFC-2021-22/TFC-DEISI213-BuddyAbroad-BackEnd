from rest_framework import serializers
from .models import *


class InterestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interests
        fields = [
            'name'
        ]

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Languages
        fields = [
            'name'
        ]


class UserSerializer(serializers.ModelSerializer):

    interests,languages = InterestsSerializer(many = True),LanguageSerializer(many=True)

    class Meta:
        model = Users
        fields = '__all__'

    def create(self, validated_data):

        interests_data = validated_data.pop('interests')
        languages_data = validated_data.pop('languages')

        user = Users.objects.create(**validated_data)

        # Create interests
        for interest_data in interests_data:
            interest_data_obj = Interests.objects.get(name=interest_data['name'])
            user.interests.add(interest_data_obj)

        # Create languages
        for lang_data in languages_data:
            lang_data_obj = Languages.objects.get(name=lang_data['name'])
            user.languages.add(lang_data_obj)

        return user

    def update(self,instance,validated_data):
        interests_data = validated_data.pop('interests')

        # Update all fields excluding interests
        instance.name = validated_data.get('name',instance.name)
        instance.save()

        return instance


class TripsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Trips
        fields = ('__all__')