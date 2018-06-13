from django.shortcuts import render
from django.db.models import Q

from rest_framework import generics

from app.models import Tweet
from app.serializers import TweetSerializer
from app.permissions import IsOwnerOrReadOnly


class TweetListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TweetSerializer

    def get_queryset(self):

        # Admin user
        if self.request.user.is_superuser:
            return Tweet.objects.all()

        # Non logged in user
        if self.request.user.id == None:
            return Tweet.objects.filter(private=False)

        # Logged in non-admin user
        return Tweet.objects.filter(
            Q(author=self.request.user) | Q(private=False)
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class TweetRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
