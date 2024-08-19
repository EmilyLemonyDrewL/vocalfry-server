# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from vocalfryapi.models import ProfileCategory

class ProfileCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileCategory
        fields = ('id', 'profile_id', 'category_id', 'profile', 'category')
        depth = 1

class ProfileCategoryView(ViewSet):

    def retrieve(self, request, pk):
        try:
            profilecategory = ProfileCategory.objects.get(pk=pk)
            serializer = ProfileCategorySerializer(profilecategory)
            return Response(serializer.data)
        except ProfileCategory.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        profilecategories = ProfileCategory.objects.all()
        serializer = ProfileCategorySerializer(profilecategories, many=True)
        return Response(serializer.data)
