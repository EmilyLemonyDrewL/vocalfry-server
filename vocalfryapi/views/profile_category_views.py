from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from vocalfryapi.models import ProfileCategory, Profile, Category

class ProfileCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileCategory
        fields = ('id', 'profile_id', 'category_id', 'category')
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
        profile_id = request.query_params.get('profileId')
        if profile_id:
            profilecategories = ProfileCategory.objects.filter(profile_id=profile_id)
        else:
          profilecategories = ProfileCategory.objects.all()
        serializer = ProfileCategorySerializer(profilecategories, many=True)
        return Response(serializer.data)

    def create(self, request):
        profile = Profile.objects.get(pk=request.data['profile'])
        category = Category.objects.get(pk=request.data['category'])

        profile_category = ProfileCategory.objects.create(
            profile=profile,
            category=category,
        )

        serializer = ProfileCategorySerializer(profile_category)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy (self, request, pk):
        try:
          profile_category = ProfileCategory.objects.get(pk=pk)
          profile_category.delete()
          return Response(status=status.HTTP_204_NO_CONTENT)
        except ProfileCategory.DoesNotExist:
          return Response({'message': 'ProfileCategory not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
        # Log the exception if needed
          print(f"An error occurred while deleting the category: {str(ex)}")
          return Response({'message': 'An error occurred while deleting the category.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
