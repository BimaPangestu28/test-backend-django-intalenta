from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Track
from .serializers import TrackSerializer
from pydub import AudioSegment
from pydub.silence import detect_silence


class TrackView(APIView):
    def post(self, request, format=None):
        serializer = TrackSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            track = serializer.save()
            return Response(track, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TrackStartTimeView(APIView):
    def post(self, request, pk, format=None):
        try:
            track = Track.objects.get(pk=pk)
        except Track.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        audio = AudioSegment.from_file(track.file.path)

        silence = detect_silence(audio, min_silence_len=1000, silence_thresh=-40)

        if len(silence) > 0:
            start_time = silence[0][1] / 1000.0
        else:
            start_time = 0.0

        return Response({"start_time": start_time}, status=status.HTTP_200_OK)
