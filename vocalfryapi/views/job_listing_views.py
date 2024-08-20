# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from vocalfryapi.models import JobListing, User

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

    def create(self, request):
        lister = User.objects.get(uid=request.data["listerId"])

        job_listing = JobListing.objects.create(
            title=request.data['title'],
            description=request.data['description'],
            location=request.data['location'],
            listing_date=request.data['listing_date'],
            company_website=request.data['company_website'],
            lister=lister,
        )
        serializer = JobListingSerializer(job_listing)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        job_listing = JobListing.objects.get(pk=pk)
        job_listing.title = request.data['title']
        job_listing.description = request.data['description']
        job_listing.location = request.data['location']
        job_listing.listing_date = request.data['listing_date']
        job_listing.company_website = request.data['company_website']

        lister = User.objects.get(uid=request.data["listerId"])
        job_listing.lister = lister
        job_listing.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
