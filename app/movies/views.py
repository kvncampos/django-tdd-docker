# Create your views here.
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ModelViewSet

from .models import Movie
from .serializers import MovieSerializer

"""
    --------------
    Using API View
    --------------
    from django.http import Http404
    from rest_framework import status
    from rest_framework.response import Response
    from rest_framework.views import APIView
    # class MovieList(APIView):
    #     def get(self, request, format=None):
    #         movies = Movie.objects.all()
    #         serializer = MovieSerializer(movies, many=True)
    #         return Response(serializer.data)

    #     def post(self, request, format=None):
    #         serializer = MovieSerializer(data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # class MovieDetail(APIView):
    #     def get_object(self, pk):
    #         try:
    #             return Movie.objects.get(pk=pk)
    #         except Movie.DoesNotExist:
    #             raise Http404

    #     def get(self, request, pk, format=None):
    #         movie = self.get_object(pk)
    #         serializer = MovieSerializer(movie)
    #         return Response(serializer.data)
"""

# Define the custom request body schema for POST and PUT requests
movie_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "title": openapi.Schema(type=openapi.TYPE_STRING, description="Title of the movie"),
        "genre": openapi.Schema(type=openapi.TYPE_STRING, description="Genre of the movie"),
        "year": openapi.Schema(type=openapi.TYPE_STRING, description="Release year of the movie"),
    },
    required=["title", "genre", "year"]  # Add required fields if needed
)

class MovieViewSet(ModelViewSet):
    """ViewSet for managing Movie instances."""

    serializer_class = MovieSerializer
    queryset = Movie.objects.all()

    @swagger_auto_schema(
        request_body=movie_request_schema,
        responses={201: MovieSerializer, 400: "Bad Request"},
    )
    def create(self, request, *args, **kwargs): # noqa: ANN001, ANN002, ANN003
        """Create a new Movie instance."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=movie_request_schema,
        responses={200: MovieSerializer, 400: "Bad Request"},
    )
    def update(self, request, *args, **kwargs):  # noqa: ANN001, ANN002, ANN003
        """Update an existing Movie instance."""
        return super().update(request, *args, **kwargs)
