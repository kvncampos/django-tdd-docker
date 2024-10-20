from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Custom user model."""


class Movie(models.Model):
    """Model representing a movie with title, genre, year, created date, and updated date.

    Attributes:
        title (str): The title of the movie.
        genre (str): The genre of the movie.
        year (str): The release year of the movie.
        created_date (datetime): The date and time when the movie record was created.
        updated_date (datetime): The date and time when the movie record was last updated.

    Methods:
        __str__: Returns the title of the movie as a string.

    """

    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    year = models.CharField(max_length=4)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:  # noqa: D105
        return f"{self.title}"
