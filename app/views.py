from django.shortcuts import render

from rest_framework import generics

from app.models import Tweet
from app.serializers import TweetSerializer
from app.permissions import IsOwnerOrReadOnly


class TweetListCreateAPIView(generics.ListCreateAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class TweetRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
