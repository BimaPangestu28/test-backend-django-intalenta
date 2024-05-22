from django.conf import settings
from rest_framework import serializers
from .models import Track


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ["id", "file", "artist", "title"]

    def get_file(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.file.url)

    def create(self, validated_data):
        track = Track.objects.create(**validated_data)
        return {
            "id": track.id,
            "file": self.get_file(track),
            "artist": track.artist,
            "title": track.title,
        }

    def validate(self, data):
        file = data.get("file", None)
        artist = data.get("artist", None)
        title = data.get("title", None)

        if file is None or artist is None or title is None:
            raise serializers.ValidationError(
                "All fields: 'file', 'artist', and 'title' must be provided."
            )

        if not file.name.endswith((".mp3", ".wav", ".flac")):
            raise serializers.ValidationError(
                "Invalid file format. Only '.mp3', '.wav', and '.flac' are allowed."
            )

        return data
