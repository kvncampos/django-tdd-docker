from unittest.mock import MagicMock

import pytest
from movies.models import Movie
from movies.serializers import MovieSerializer


@pytest.fixture(scope="function")
def add_movie():
    def _add_movie(title, genre, year):
        movie = Movie.objects.create(title=title, genre=genre, year=year)
        return movie

    return _add_movie


@pytest.fixture
def mock_movie():
    """Fixture for a mock Movie object."""
    movie = MagicMock()
    movie.id = 1
    movie.title = "The Big Lebowski"
    movie.genre = "comedy"
    movie.year = "1998"
    return movie


@pytest.fixture
def mock_serializer(mock_movie):
    """Fixture for a mock MovieSerializer."""
    serializer = MagicMock(spec=MovieSerializer)
    serializer.data = {
        "id": mock_movie.id,
        "title": mock_movie.title,
        "genre": mock_movie.genre,
        "year": mock_movie.year,
    }
    return serializer
