from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..serializers import *


class InterestsAPI(generics.ListCreateAPIView):
    queryset = Interests.objects.all()
    serializer_class = InterestsSerializer

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
