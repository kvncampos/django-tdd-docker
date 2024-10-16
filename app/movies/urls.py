# myapp/urls.py
from django.http import JsonResponse
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MovieViewSet

# Create a router and register the MovieViewSet
router = DefaultRouter()
router.register(r"api/movies", MovieViewSet, basename="movie")


def ping(request):
    return JsonResponse({"message": "pong"})


# Include the router's URLs
urlpatterns = [
    path("", include(router.urls)),
    path("ping/", ping, name="ping"),
]
