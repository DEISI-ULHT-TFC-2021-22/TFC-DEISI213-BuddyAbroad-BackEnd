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


class InterestCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestCategories
        fields = [
            'name'
        ]


class UserSerializer(serializers.ModelSerializer):
    interests, languages = InterestsSerializer(many=True), LanguageSerializer(many=True)

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

    def update(self, instance, validated_data):
        interests_data = validated_data.pop('interests')
        languages_data = validated_data.pop('languages')

        instance = super().update(instance, validated_data)
        instance.interests.clear()
        instance.languages.clear()

        for interest_data in interests_data:
            interest_data_obj = Interests.objects.get(name=interest_data['name'])
            instance.interests.add(interest_data_obj)

        for language_data in languages_data:
            language_data_obj = Languages.objects.get(name=language_data['name'])
            instance.languages.add(language_data_obj)

        return instance


class TripsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Trips
        fields = '__all__'


class InterestPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestPoints
        geo_field = "point"
        fields = '__all__'


class UserTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTrips
        fields = '__all__'

class FavouritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourites
        fields = '__all__'
