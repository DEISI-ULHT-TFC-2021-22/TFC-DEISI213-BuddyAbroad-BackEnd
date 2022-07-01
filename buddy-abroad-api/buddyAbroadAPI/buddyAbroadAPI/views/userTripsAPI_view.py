import boto3
from botocore.exceptions import ClientError
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..serializers import *
from ..models import *


class UserTripsAPI:

    @api_view(['POST'])
    def post_user_trips(request):
        user_trips = UserTripSerializer(data=request.data)

        if user_trips.is_valid():
            user_trips.save()
            return Response(user_trips.data, status=status.HTTP_201_CREATED)
        else:
            return Response(user_trips.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET', 'PUT', 'DELETE'])
    def user_trips_get_update_delete(request, id):
        if request.method == 'GET':
            user_trips = UserTrips.objects.all().filter(pk=id)
            if len(user_trips) > 0:
                user_trips_serializer = UserTripSerializer(user_trips, many=True)
                return Response(user_trips_serializer.data)
            else:
                return Response({
                    'msg': 'Não existem user trips que correspondam com o id ' + str(id)
                })
        elif request.method == 'PUT':
            if id:
                user_trips = UserTrips.objects.get(pk=id)
                user_trips_serializer = UserTripSerializer(instance=user_trips, data=request.data, partial=True)
                if user_trips_serializer.is_valid():
                    # Updating user trips
                    user_trips_serializer.save()
                    return Response(user_trips_serializer.data, status=200)
                return Response(user_trips_serializer.errors, status=400)
            return Response('Missing ID', status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            user_trips = UserTrips.objects.get(pk=id)
            operation = user_trips.delete()
            data = {}
            if operation:
                data['success'] = 'delete successful'
            else:
                data['failure'] = 'delete failed'
            return Response(data=data)

    @api_view(['GET'])
    def get_user_bookings(request, id):
        user_trips = UserTrips.objects.filter(tourist=id)

        user_trips_serializer = UserTripSerializer(user_trips, many=True)

        return Response(user_trips_serializer.data, status=status.HTTP_201_CREATED)

    @api_view(['GET'])
    def get_trips_user_bookings(request, id):
        boto3.setup_default_session(region_name='eu-west-2')
        client = boto3.client('s3')
        user_trips = UserTrips.objects.filter(tourist=id)
        data = []

        for user_trip in user_trips:
            data.append(Trips.objects.get(pk=user_trip.reference_id))

        for trip in data:
            try:
                response = client.generate_presigned_url(ClientMethod='get_object',
                                                         Params={'Bucket': 'buddy-abroad-files',
                                                                 'Key': str(trip.imageName)},
                                                         ExpiresIn=3600)
                trip.imageURL = response
            except ClientError as e:
                return Response(e)

        trips_serializer = TripsSerializers(data, many=True)

        return Response(trips_serializer.data, status=status.HTTP_201_CREATED)

    @api_view(['DELETE'])
    def favourite_delete(request, id):
        favourite_trips = Favourites.objects.get(pk=id)
        operation = favourite_trips.delete()
        data = {}
        if operation:
            data['success'] = 'delete successful'
        else:
            data['failure'] = 'delete failed'
        return Response(data=data)

    @api_view(['POST'])
    def post_user_favourites(request):
        favourite_trips = FavouritesSerializer(data=request.data)
        user_favourites = Favourites.objects.all().filter(user_id=request.data['user_id'])

        for user_favourite in user_favourites:
            if user_favourite.trip_id_id == int((request.data['trip_id'])):
                return Response({
                    'msg': 'Esta trip já se encontra nos favoritos'
                })

        if favourite_trips.is_valid():
            favourite_trips.save()
            return Response(favourite_trips.data, status=status.HTTP_201_CREATED)
        else:
            return Response(favourite_trips.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET'])
    def get_object_favourites(request, id):
        if request.method == 'GET':
            # buscar objetos favoritos pelo id do user
            user_favourites = Favourites.objects.all().filter(user_id=id)
            if len(user_favourites) > 0:
                favourites_serializer = FavouritesSerializer(user_favourites, many=True)

                return Response(favourites_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'msg': 'Este utilizador ainda não tem favoritos'
                })

    @api_view(['GET'])
    def get_trips_favourites(request, id):
        if request.method == 'GET':
            # buscar trips dos favoritos pelo id do user
            boto3.setup_default_session(region_name='eu-west-2')
            client = boto3.client('s3')
            user_favourites = Favourites.objects.all().filter(user_id=id)
            if len(user_favourites) > 0:
                data = []

                for user_favourite in user_favourites:
                    data.append(Trips.objects.all().get(pk=user_favourite.trip_id_id))

                for trip in data:

                    try:
                        response = client.generate_presigned_url(ClientMethod='get_object',
                                                                 Params={'Bucket': 'buddy-abroad-files',
                                                                         'Key': str(trip.imageName)},
                                                                 ExpiresIn=3600)
                        trip.imageURL = response
                    except ClientError as e:
                        return Response(e)

                trips_serializer = TripsSerializers(data, many=True)

                return Response(trips_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'msg': 'Este utilizador ainda não tem favoritos'
                })
