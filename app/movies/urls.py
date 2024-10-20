# myapp/urls.py
from django.http import JsonResponse
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MovieViewSet

# Create a router and register the MovieViewSet
router = DefaultRouter()
router.register(r"api/movies", MovieViewSet, basename="movie")


# Include the router's URLs
urlpatterns = [
    path("", include(router.urls)),
]
