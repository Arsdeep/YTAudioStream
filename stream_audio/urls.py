from django.urls import path
from .views import stream_audio

urlpatterns = [
    path('stream-audio/', stream_audio, name='stream_audio'),
]