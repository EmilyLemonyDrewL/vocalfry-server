# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from vocalfryapi.models import Profile, ProfileCategory, User
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

    def create(self, request):
        user = User.objects.get(uid=request.data['userId'])

        profile = Profile.objects.create(
            name_seen_on_profile=request.data['name_seen_on_profile'],
            image_url=request.data['image_url'],
            bio=request.data['bio'],
            location=request.data['location'],
            above_18=request.data['above_18'],
            work_remote=request.data['work_remote'],
            demo_reel_url=request.data['demo_reel_url'],
            email=request.data['email'],
            phone=request.data['phone'],
            user=user,
        )

        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        profile = Profile.objects.get(pk=pk)
        profile.name_seen_on_profile = request.data['name_seen_on_profile']
        profile.image_url = request.data['image_url']
        profile.bio = request.data['bio']
        profile.location = request.data['location']
        profile.above_18 = request.data['above_18']
        profile.work_remote = request.data['work_remote']
        profile.demo_reel_url = request.data['demo_reel_url']
        profile.email = request.data['email']
        profile.phone = request.data['phone']

        user = User.objects.get(uid=request.data['userId'])
        profile.user = user
        profile.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy (self, request, pk):
        profile = Profile.objects.get(pk=pk)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
