from django.urls import path
from .views import TrackView, TrackStartTimeView

urlpatterns = [
    path("api/tracks/", TrackView.as_view(), name="track-upload"),
    path(
        "api/tracks/<int:pk>/calculate-start-time/",
        TrackStartTimeView.as_view(),
        name="track-start-time",
    ),
]
