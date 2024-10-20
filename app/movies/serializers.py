from rest_framework import serializers

from .models import Movie


class MovieSerializer(serializers.ModelSerializer):
    """Serializer for the Movie model.

    Attributes:
        model: Movie - The model class being serialized.
        fields: All fields of the Movie model are included for serialization.
        read_only_fields: Certain fields like id, created_date, and updated_date are read-only during serialization.

    """

    class Meta:  # noqa: D106
        model = Movie
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_date",
            "updated_date",
        )
