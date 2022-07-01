from botocore.exceptions import ClientError
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from ..serializers import *
from ..models import *
import boto3
from environs import Env

# Documentation

env = Env()
env.read_env()


class UsersAPI(APIView):

    @api_view(['GET', 'POST'])
    def users_list_create(request):

        if request.method == 'GET':
            # Listing all the users from RDS
            users = Users.objects.all()
            users_serializer = UserSerializer(users, many=True)
            return Response(users_serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'POST':
            # Create a new user
            user = UserSerializer(data=request.data)
            if user.is_valid():
                user.save()  # Save User on DataBase
                return Response(user.data, status=status.HTTP_201_CREATED)
            else:
                return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET', 'PUT', 'DELETE'])
    def user_get_update_delete(request, id):
        if request.method == 'PUT':
            if id:
                user = Users.objects.get(pk=id)
                user_serializer = UserSerializer(instance=user, data=request.data, partial=True)
                if user_serializer.is_valid():
                    # Updating object
                    user_serializer.save()

                    return Response(user_serializer.data, status=200)
                return Response(user_serializer.errors, status=400)
            return Response('Missing ID', status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'GET':
            user = Users.objects.get(pk=id)
            if user is not None:
                boto3.setup_default_session(region_name='eu-west-2')
                client = boto3.client('s3')
                user_serializer = UserSerializer(user)
                try:
                    response = client.generate_presigned_url(ClientMethod='get_object',
                                                             Params={'Bucket': 'buddy-abroad-files',
                                                                     'Key': str(user.imageName)},
                                                             ExpiresIn=3600)
                    user.imageURL = response
                except ClientError as e:
                    return Response(e)
                return Response(user_serializer.data, status=200)
        elif request.method == 'DELETE':
            user = Users.objects.get(pk=id)
            operation = user.delete()
            data = {}
            if operation:
                data['success'] = 'Delete successful'
            else:
                data['failure'] = 'Delete failed'
            return Response(data=data)

    @api_view(['GET'])
    def get_user_by_email(request, email):
        user = Users.objects.get(email=email)
        if user is not None:
            boto3.setup_default_session(region_name='eu-west-2')
            client = boto3.client('s3')

            try:
                response = client.generate_presigned_url(ClientMethod='get_object',
                                                         Params={'Bucket': 'buddy-abroad-files',
                                                                 'Key': str(user.imageName)},
                                                         ExpiresIn=3600)
                user.imageURL = response
            except ClientError as e:
                return Response(e)
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data, status=200)

    @api_view(['GET'])
    def api_root(request, format=None):
        return Response({
            'Users': reverse('users', request=request, format=format),
            # 'Users Get Update Delete by id': reverse('user_get_update_delete', request=request, format=format),
            'Trips': reverse('trips', request=request, format=format),
            # 'Users by Email': reverse('get_user_by_email', request=request, format=format),
            # 'Trips Get Update Delete by id': reverse('trip_get_update_delete', request=request, format=format),
            'Signup': reverse('sign_up', request=request, format=format),
            'Confirm Signup': reverse('confirm_sign_up', request=request, format=format),
            'Login': reverse('login_auth', request=request, format=format),
            'Forgot Password': reverse('forgot_password', request=request, format=format),
            'Confirm Forgot Password': reverse('confirm_forgot_password', request=request, format=format),
            'Change Password': reverse('change_password', request=request, format=format),
            'Translate': reverse('translate', request=request, format=format),
            'documentation': reverse('schema-swagger-ui', request=request, format=format),
        })
