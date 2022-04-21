from botocore.exceptions import ClientError
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .serializers import *
import boto3
import hashlib
import hmac
import base64
from environs import Env
# Documentation
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

env = Env()
env.read_env()

from .models import *


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
                user_serializer = UserSerializer(instance=user, data=request.data)
                if user_serializer.is_valid():
                    # Updating object
                    user_serializer.save()

                    return Response(user_serializer.data, status=200)
                return Response(user_serializer.errors, status=400)
            return Response('Missing ID', status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'GET':
            user = Users.objects.get(pk=id)
            if user is not None:
                user_serializer = UserSerializer(user)
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
        if request.method == 'GET':
            user = Users.objects.get(email=email)
            if user is not None:
                user_serializer = UserSerializer(user)
                return Response(user_serializer.data, status=200)

    @api_view(['POST'])
    def get_interests_by_categories(request):
        if request.method == 'POST':
            categories = InterestCategories.objects.all()
            interests = Interests.objects.all()
            interests2 = []
            exists = 0

            for category in categories:
                if category.name == request.data['category']:
                    exists = 1
                    category_id = category.id

            if exists:
                for interest in interests:
                    if interest.category_id == category_id:
                        interests2.append(interest)

                interests_serializer = InterestsSerializer(interests2, many=True)
                return Response(interests_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response('Category does not exist')

    @swagger_auto_schema(method='post', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        }
    ))
    @api_view(['POST'])
    def sign_up(request):
        boto3.setup_default_session(region_name='eu-west-2')
        client = boto3.client('cognito-idp')

        key = bytes(env.str('APP_CLIENT_SECRET'), "utf-8")
        msg = bytes(request.data['email'] + env.str('AWS_CLIENT_ID'), "utf-8")

        new_digest = hmac.new(key, msg, hashlib.sha256).digest()
        SECRET_HASH = base64.b64encode(new_digest).decode()

        try:
            # Add user to pool
            sign_up_response = client.sign_up(
                ClientId=env.str('AWS_CLIENT_ID'),
                Username=request.data['email'],
                Password=request.data['password'],
                SecretHash=SECRET_HASH,
                UserAttributes=[
                    {
                        'Name': "email",
                        'Value': request.data['email']
                    },
                    {
                        'Name': "name",
                        'Value': ""
                    }
                ])

            return Response(
                {
                    'MSG': 'User created!',
                    'response': sign_up_response
                })

        except client.exceptions.InvalidPasswordException:
            return Response('Error:Invalid password! Password must have length 8 with numbers and special characters')
        except client.exceptions.UsernameExistsException:
            return Response('Error:Username already exists!')
        except client.exceptions.ResourceNotFoundException:
            return Response('Error:Resource not found')
        except client.exceptions.CodeDeliveryFailureException:
            return Response('Error:Code has not been delivered')

    @swagger_auto_schema(method='post', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
            'code': openapi.Schema(type=openapi.TYPE_STRING, description='int'),
        }
    ))
    @api_view(['POST'])
    def confirm_sign_up(request):
        boto3.setup_default_session(region_name='eu-west-2')
        client = boto3.client('cognito-idp')

        key = bytes(env.str('APP_CLIENT_SECRET'), "utf-8")
        msg = bytes(request.data['email'] + env.str('AWS_CLIENT_ID'), "utf-8")

        new_digest = hmac.new(key, msg, hashlib.sha256).digest()
        SECRET_HASH = base64.b64encode(new_digest).decode()

        try:
            response = client.confirm_sign_up(
                ClientId=env.str('AWS_CLIENT_ID'),
                SecretHash=SECRET_HASH,
                Username=request.data['email'],
                ConfirmationCode=request.data['code'],
            )

            return Response({
                'MSG': 'User Confirmed',
                'response': response
            })
        except client.exceptions.CodeMismatchException:
            return Response('Error: Code mismatch')
        except client.exceptions.ExpiredCodeException:
            return Response('Error: Code has expired')
        except client.exceptions.UserNotFoundException:
            return Response('Error: User not found')

    @swagger_auto_schema(method='post', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        }
    ))
    @api_view(['POST'])
    def login_auth(request):
        boto3.setup_default_session(region_name='eu-west-2')
        client = boto3.client('cognito-idp')

        key = bytes(env.str('APP_CLIENT_SECRET'), "utf-8")
        msg = bytes(request.data['email'] + env.str('AWS_CLIENT_ID'), "utf-8")

        new_digest = hmac.new(key, msg, hashlib.sha256).digest()
        SECRET_HASH = base64.b64encode(new_digest).decode()

        try:
            response = client.initiate_auth(
                ClientId=env.str('AWS_CLIENT_ID'),
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': request.data['email'],
                    'PASSWORD': request.data['password'],
                    'SECRET_HASH': SECRET_HASH
                },
            )
            return Response({
                'MSG': 'User Confirmed',
                'response': response,
            })
        except client.exceptions.UserNotFoundException:
            return Response('Error: User not found')
        except client.exceptions.UserNotConfirmedException:
            return Response('Error: User not confirmed')
        except client.exceptions.NotAuthorizedException:
            return Response('Error: Incorrect username or password!')

    @api_view(['POST'])
    def forgot_password(request):
        boto3.setup_default_session(region_name='eu-west-2')
        client = boto3.client('cognito-idp')

        key = bytes(env.str('APP_CLIENT_SECRET'), "utf-8")
        msg = bytes(request.data['username'] + env.str('AWS_CLIENT_ID'), "utf-8")
        new_digest = hmac.new(key, msg, hashlib.sha256).digest()
        SECRET_HASH = base64.b64encode(new_digest).decode()
        try:
            response = client.forgot_password(
                ClientId=env.str('AWS_CLIENT_ID'),
                Username=request.data['username'],
                SecretHash=SECRET_HASH
            )
            return Response({
                'response': response,
            })
        except client.exceptions.CodeDeliveryFailureException:
            return Response('Error: Code delivery failure')
        except client.exceptions.UserNotFoundException:
            return Response('Error: User not found')

    @api_view(['POST'])
    def confirm_forgot_password(request):
        boto3.setup_default_session(region_name='eu-west-2')
        client = boto3.client('cognito-idp')

        key = bytes(env.str('APP_CLIENT_SECRET'), "utf-8")
        msg = bytes(request.data['username'] + env.str('AWS_CLIENT_ID'), "utf-8")
        new_digest = hmac.new(key, msg, hashlib.sha256).digest()
        SECRET_HASH = base64.b64encode(new_digest).decode()

        try:
            response = client.confirm_forgot_password(
                ClientId=env.str('AWS_CLIENT_ID'),
                Username=request.data['username'],
                ConfirmationCode=request.data['confirm_code'],
                Password=request.data['password'],
                SecretHash=SECRET_HASH
            )
            return Response({
                'response': response,
            })
        except client.exceptions.CodeMismatchException:
            return Response('Error: Confirmation code does not match')
        except client.exceptions.ExpiredCodeException:
            return Response('Error: Confirmation code has expired')
        except client.exceptions.InvalidPasswordException:
            return Response('Error: Invalid password')
        except client.exceptions.UserNotFoundException:
            return Response('Error: User not found')

    @api_view(['POST'])
    def change_password(request):
        boto3.setup_default_session(region_name='eu-west-2')
        client = boto3.client('cognito-idp')
        try:
            response = client.change_password(
                PreviousPassword=request.data['previous_password'],
                ProposedPassword=request.data['proposed_password'],
                AccessToken=request.data['access_token'],
            )
            return Response({
                'response': response,
            })
        except client.exceptions.InvalidPasswordException:
            return Response('Error: Invalid password')
        except client.exceptions.UserNotFoundException:
            return Response('Error: User not found')


class InterestsAPI(generics.ListCreateAPIView):
    queryset = Interests.objects.all()
    serializer_class = InterestsSerializer


class AwsTranslate:
    @api_view(['POST'])
    def translate(request):
        boto3.setup_default_session(region_name='eu-west-2')
        translate = boto3.client(service_name='translate')

        result = translate.translate_text(
            Text=request.data['text'],
            SourceLanguageCode=request.data['sourceLanguageCode'],
            TargetLanguageCode=request.data['targetLanguageCode']
        )

        return JsonResponse(result)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'Users': reverse('users', request=request, format=format),
        #'Users Get Update Delete by id': reverse('user_get_update_delete', request=request, format=format),
        'Trips': reverse('trips', request=request, format=format),
        #'Users by Email': reverse('get_user_by_email', request=request, format=format),
        'Post Trip': reverse('post_trip', request=request, format=format),
        #'Trips Get Update Delete by id': reverse('trip_get_update_delete', request=request, format=format),
        'Signup': reverse('sign_up', request=request, format=format),
        'Confirm Signup': reverse('confirm_sign_up', request=request, format=format),
        'Login': reverse('login_auth', request=request, format=format),
        'Forgot Password': reverse('forgot_password', request=request, format=format),
        'Confirm Forgot Password': reverse('confirm_forgot_password', request=request, format=format),
        'Change Password': reverse('change_password', request=request, format=format),
        'Translate': reverse('translate', request=request, format=format),
        'documentation': reverse('schema-swagger-ui', request=request, format=format),
    })
