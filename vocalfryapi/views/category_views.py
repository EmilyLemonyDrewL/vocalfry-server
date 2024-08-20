# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from vocalfryapi.models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'label')
        depth = 1

class CategoryView(ViewSet):

    def retrieve(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def create(self, request):
        category = Category.objects.create(
            label=request.data['label']
        )
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        category = Category.objects.get(pk=pk)
        category.label = request.data['label']
        category.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
