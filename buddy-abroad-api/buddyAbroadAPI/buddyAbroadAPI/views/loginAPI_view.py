from rest_framework.decorators import api_view
from rest_framework.response import Response
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


class LoginAPI:

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
