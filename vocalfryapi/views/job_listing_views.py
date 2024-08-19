# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from vocalfryapi.models import JobListing

class JobListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobListing
        fields = ('id', 'lister_id', 'title', 'description', 'location', 'listing_date', 'company_website', 'lister')
        depth = 1

class JobListingView(ViewSet):

    def retrieve(self, request, pk):
        try:
            job_listing = JobListing.objects.get(pk=pk)
            serializer = JobListingSerializer(job_listing)
            return Response(serializer.data)
        except JobListing.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        job_listings = JobListing.objects.all()
        serializer = JobListingSerializer(job_listings, many=True)
        return Response(serializer.data)
