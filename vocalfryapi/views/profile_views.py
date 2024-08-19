# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from vocalfryapi.models import Profile, ProfileCategory
from .profile_category_views import ProfileCategorySerializer

class ProfileSerializer(serializers.ModelSerializer):
    profile_category = ProfileCategorySerializer(read_only=True)
    class Meta:
        model = Profile
        fields = ('id', 'user_id', 'name_seen_on_profile', 'image_url', 'bio', 'location', 'above_18', 'work_remote', 'demo_reel_url', 'email', 'phone', 'profile_category', 'user')
        depth = 1

class ProfileView(ViewSet):

    def retrieve(self, request, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        category_id = request.query_params.get('category_id', None)

        if category_id is not None:
            profile_categories = ProfileCategory.objects.filter(category_id=category_id)
            profiles = Profile.objects.filter(id__in=profile_categories.values_list('profile_id', flat=True))
        else:
            profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)
