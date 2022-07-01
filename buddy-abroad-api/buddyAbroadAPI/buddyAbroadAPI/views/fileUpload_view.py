import logging

import boto3
from botocore.exceptions import ClientError
from rest_framework.decorators import api_view


class FileUpload:
    @api_view(['POST'])
    def upload_file(request):

        s3_client = boto3.client('s3')
        try:
            s3_client.upload_fileobj(request.FILES['file'], 'buddy-abroad-files', request.data['name'])

        except ClientError as e:
            logging.error(e)
            return False
        return True
