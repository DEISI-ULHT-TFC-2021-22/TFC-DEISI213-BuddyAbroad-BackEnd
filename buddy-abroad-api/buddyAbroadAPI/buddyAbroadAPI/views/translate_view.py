import boto3
from django.http import JsonResponse
from rest_framework.decorators import api_view


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
