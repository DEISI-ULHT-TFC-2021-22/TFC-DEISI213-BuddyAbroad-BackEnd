import logging
import os

from botocore.exceptions import ClientError
from django.http import JsonResponse
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
import boto3
from environs import Env
# Documentation
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from ..serializers import *
from ..models import *

env = Env()
env.read_env()


class TripsAPI(generics.ListCreateAPIView):
    test_param = openapi.Parameter('test', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_BOOLEAN)
    trips_response = openapi.Response('response description', TripsSerializers)

    @swagger_auto_schema(methods=['get'],
                         manual_parameters=[test_param],
                         responses={200: trips_response})
    @api_view(['GET'])
    def get_trips(request):
        trips = Trips.objects.all()
        boto3.setup_default_session(region_name='eu-west-2')
        client = boto3.client('s3')
        for trip in trips:
            try:
                response = client.generate_presigned_url(ClientMethod='get_object',
                                                         Params={'Bucket': 'buddy-abroad-files',
                                                                 'Key': str(trip.imageName)},
                                                         ExpiresIn=3600)
                trip.imageURL = response
            except ClientError as e:
                return Response(e)
        trips_serializer = TripsSerializers(trips, many=True)
        return Response(trips_serializer.data)

    @api_view(['GET', 'PUT', 'DELETE'])
    def trip_get_update_delete(request, id):
        if request.method == 'GET':
            trips = Trips.objects.all().filter(pk=id)
            if len(trips) > 0:
                trips_serializer = TripsSerializers(trips, many=True)
                return Response(trips_serializer.data)
            else:
                return Response({
                    'msg': 'Não existem trips que correspondem com o id ' + str(id)
                })
        elif request.method == 'PUT':
            if id:
                trips = Trips.objects.get(pk=id)
                trips_serializer = TripsSerializers(instance=trips, data=request.data, partial=True)
                if trips_serializer.is_valid():
                    # Updating trips
                    trips_serializer.save()
                    return Response(trips_serializer.data, status=200)
                return Response(trips_serializer.errors, status=400)
            return Response('Missing ID', status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            trips = Trips.objects.get(pk=id)
            operation = trips.delete()
            data = {}
            if operation:
                data['success'] = 'delete successful'
            else:
                data['failure'] = 'delete failed'
            return Response(data=data)

    @api_view(['POST'])
    def post_trip(request):
        if request.method == 'POST':
            data = JSONParser().parse(request)
            trip_serializer = TripsSerializers(data=data)

            if trip_serializer.is_valid():
                trip_serializer.save()
                return JsonResponse(trip_serializer.data, status=status.HTTP_201_CREATED)

            return JsonResponse(trip_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse("Bad Request", status=status.HTTP_400_BAD_REQUEST)

    @api_view(['POST', 'GET'])
    def interest_points_list_create(request):
        if request.method == 'GET':
            interest_points = InterestPoints.objects.all()
            interest_points_serializer = InterestPointSerializer(interest_points, many=True)
            return Response(interest_points_serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'POST':
            interest_points_serializer = InterestPointSerializer(data=request.data)

            if interest_points_serializer.is_valid():
                interest_points_serializer.save()
                return Response(interest_points_serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse(interest_points_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET', 'PUT', 'DELETE'])
    def interest_point_get_update_delete(request, id):
        if request.method == 'GET':
            interest_points = InterestPoints.objects.all().filter(pk=id)
            if len(interest_points) > 0:
                interest_points_serializer = InterestPointSerializer(interest_points, many=True)
                return Response(interest_points_serializer.data)
            else:
                return Response({
                    'msg': 'Não existem pontos de interesse que correspondam com o id ' + str(id)
                })
        elif request.method == 'PUT':
            if id:
                interest_points = InterestPoints.objects.get(pk=id)
                interest_points_serializer = InterestPointSerializer(instance=interest_points, data=request.data,
                                                                     partial=True)
                if interest_points_serializer.is_valid():
                    # Updating pontos de interesse
                    interest_points_serializer.save()
                    return Response(interest_points_serializer.data, status=200)
                return Response(interest_points_serializer.errors, status=400)
            return Response('Missing ID', status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            interest_points = InterestPoints.objects.get(pk=id)
            operation = interest_points.delete()
            data = {}
            if operation:
                data['success'] = 'delete successful'
            else:
                data['failure'] = 'delete failed'
            return Response(data=data)

    @api_view(['GET'])
    def get_trip_interest_points(request, id):
        interest_points = InterestPoints.objects.filter(trip_id=id)

        interest_points_serializer = InterestPointSerializer(interest_points, many=True)

        return Response(interest_points_serializer.data, status=status.HTTP_201_CREATED)

    @api_view(['POST'])
    def trip_search(request):
        boto3.setup_default_session(region_name='eu-west-2')
        client = boto3.client('s3')

        querySet = Trips.objects.filter(
            Q(locationName__icontains=request.data['string']) | Q(name__icontains=request.data['string']))

        for trip in querySet:
            try:
                response = client.generate_presigned_url(ClientMethod='get_object',
                                                         Params={'Bucket': 'buddy-abroad-files',
                                                                 'Key': str(trip.imageName)},
                                                         ExpiresIn=3600)
                trip.imageURL = response
            except ClientError as e:
                return Response(e)

        trips_serializer = TripsSerializers(querySet, many=True)

        return Response(trips_serializer.data)
