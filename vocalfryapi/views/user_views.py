from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import serializers, status
from vocalfryapi.models import User
from .profile_views import ProfileSerializer
from .job_listing_views import JobListingSerializer

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    job_listings = JobListingSerializer(many=True, read_only=True, source='joblisting_set')
    class Meta:
        model = User
        fields = ('id', 'uid', 'first_name', 'last_name', 'user_type', 'profile', 'job_listings')
        depth = 1

class UserView(ViewSet):

    def retrieve(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def create(self, request):
        user = User.objects.create(
            uid=request.data['uid'],
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],
            user_type=request.data['user_type']
        )
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.uid = request.data['uid']
            user.first_name = request.data['first_name']
            user.last_name = request.data['last_name']
            user.user_type = request.data['user_type']
            user.save()

            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'messag': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def destroy (self, request, pk):
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def check_user(request):
    uid = request.data['uid']
    user = User.objects.filter(uid=uid).first()

    if user is not None:
        data = {
            'id': user.id,
            'uid': user.uid,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'user_type': user.user_type
        }
        return Response(data)
    else:
        data = {'valid': False}
        return Response(data)

@api_view(['POST'])
def register_user(request):
    user = User.objects.create(
        uid=request.data['uid'],
        first_name=request.data['first_name'],
        last_name=request.data['last_name'],
        user_type=request.data['user_type']
    )

    data = {
        'id': user.id,
        'uid': user.uid,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'user_type': user.user_type
    }
    return Response(data)
