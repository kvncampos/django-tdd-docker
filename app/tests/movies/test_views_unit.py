# # app/tests/movies/test_views_unit.py
# from unittest.mock import Mock
# import pytest
# from django.http import Http404
# from movies.models import Movie
# from movies.serializers import MovieSerializer
# from movies.views import MovieViewSet


# # ------------------------------------------
# # POST Tests
# # ------------------------------------------
# def test_add_movie(client, monkeypatch):
#     payload = {"title": "The Big Lebowski", "genre": "comedy", "year": "1998"}

#     def mock_create(self, payload):
#         return "The Big Lebowski"

#     monkeypatch.setattr(MovieSerializer, "create", mock_create)
#     monkeypatch.setattr(MovieSerializer, "data", payload)

#     resp = client.post("/api/movies/", payload, content_type="application/json")
#     assert resp.status_code == 201
#     assert resp.data["title"] == "The Big Lebowski"


# @pytest.mark.parametrize(
#     "payload, status_code",
#     [
#         [{}, 400],
#         [{"title": "The Big Lebowski", "genre": "comedy"}, 400],
#     ],
# )
# def test_add_movie_invalid_json(client, payload, status_code):
#     resp = client.post("/api/movies/", payload, content_type="application/json")
#     assert resp.status_code == status_code


# # ------------------------------------------
# # GET Tests
# # ------------------------------------------
# def test_get_single_movie(client, monkeypatch, mock_movie, mock_serializer):
#     monkeypatch.setattr(MovieViewSet, "get_object", lambda self: mock_movie)
#     monkeypatch.setattr(MovieSerializer, "data", mock_serializer.data)

#     resp = client.get("/api/movies/1/")
#     assert resp.status_code == 200
#     assert resp.data["title"] == "The Big Lebowski"


# def test_get_single_movie_incorrect_id(client):
#     resp = client.get("/api/movies/foo/")
#     assert resp.status_code == 404


# # ------------------------------------------
# # DELETE Tests
# # ------------------------------------------
# def test_delete_movie(client, monkeypatch, mock_movie):
#     monkeypatch.setattr(MovieViewSet, "get_object", lambda self: mock_movie)
#     monkeypatch.setattr(mock_movie, "delete", lambda: None)  # Mock delete method

#     resp = client.delete("/api/movies/1/")
#     assert resp.status_code == 204


# def test_remove_movie_incorrect_id(client, monkeypatch):
#     # Create a mock function that raises Http404
#     mock_get_object = Mock(side_effect=Http404)

#     # Patch the get_object method of MovieViewSet
#     monkeypatch.setattr(MovieViewSet, "get_object", mock_get_object)

#     # Send DELETE request to a non-existent ID
#     resp = client.delete("/api/movies/99/")
#     assert resp.status_code == 404


# # ------------------------------------------
# # PUT Tests
# # ------------------------------------------
# def test_update_movie(client, monkeypatch, mock_movie):
#     payload = {"title": "The Big Lebowski", "genre": "comedy", "year": "1997"}

#     def mock_update_object(self, movie_object, data):
#         return payload

#     monkeypatch.setattr(MovieViewSet, "get_object", lambda self: mock_movie)
#     monkeypatch.setattr(MovieSerializer, "update", mock_update_object)

#     resp = client.put(
#         "/api/movies/1/",
#         payload,
#         content_type="application/json",
#     )
#     assert resp.status_code == 200
#     assert resp.data["title"] == payload["title"]
#     assert resp.data["year"] == payload["year"]


# def test_update_movie_incorrect_id(client, monkeypatch):
#     # Create a mock function that raises Http404
#     mock_get_object = Mock(side_effect=Http404)

#     monkeypatch.setattr(MovieViewSet, "get_object", mock_get_object)

#     resp = client.put("/api/movies/99/")
#     assert resp.status_code == 404


# @pytest.mark.parametrize(
#     "payload, status_code",
#     [[{}, 400], [{"title": "The Big Lebowski", "genre": "comedy"}, 400]],
# )
# def test_update_movie_invalid_json(
#     client, monkeypatch, payload, status_code, mock_movie
# ):

#     monkeypatch.setattr(MovieViewSet, "get_object", lambda self: mock_movie)

#     resp = client.put(
#         "/api/movies/1/",
#         payload,
#         content_type="application/json",
#     )
#     assert resp.status_code == status_code
