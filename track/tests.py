from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Track

import os


class TrackTests(APITestCase):
    def setUp(self):
        with open("./test_files/file.mp3", "rb") as f:
            file_content = f.read()

        file = SimpleUploadedFile("./test_files/file.mp3", file_content)
        self.track = Track.objects.create(
            title="Test Track",
            artist="Test Artist",
            file=file,
        )

    def test_create_track(self):
        """
        Ensure we can create a new track object.
        """
        url = reverse("track-upload")
        data = {
            "file": SimpleUploadedFile(
                "test.mp3", b"file_content", content_type="audio/mpeg"
            ),
            "artist": "Test Artist",
            "title": "Test Title",
        }
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Track.objects.count(), 2)
        self.assertEqual(Track.objects.order_by("-id").first().artist, "Test Artist")

    def test_create_track_invalid_file_type(self):
        """
        Ensure we can't create a new track object with an invalid file type.
        """
        url = reverse("track-upload")
        data = {
            "file": SimpleUploadedFile(
                "test.txt", b"file_content", content_type="text/plain"
            ),
            "artist": "Test Artist",
            "title": "Test Title",
        }
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_track_missing_fields(self):
        """
        Ensure we can't create a new track object with missing fields.
        """
        url = reverse("track-upload")
        data = {
            "file": SimpleUploadedFile(
                "test.mp3", b"file_content", content_type="audio/mpeg"
            ),
            "artist": "Test Artist",
        }
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_calculate_start_time(self):
        """
        Ensure we can calculate the start time of a track.
        """
        url = reverse("track-start-time", args=[self.track.id])
        print(url)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        os.remove(self.track.file.path)
