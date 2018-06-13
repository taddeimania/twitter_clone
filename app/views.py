from django.shortcuts import render
from django.db.models import Q

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from app.models import Tweet, Like
from app.serializers import TweetSerializer, LikeSerializer
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


class LikeCreateDestroyAPIView(APIView):

    def post(self, request):
        user = self.request.user
        tweet_id = request.POST['tweet']
        do_i_like = Like.objects.filter(user=user, tweet_id=tweet_id).count()
        if do_i_like == 0:
            like = Like.objects.create(user=user, tweet_id=tweet_id)
            serialized_like = LikeSerializer(like)
            return Response(serialized_like.data, 201)
        raise PermissionDenied(detail="You have already liked that tweet")

    def delete(self, request):
        user = self.request.user
        tweet_id = request.POST['tweet']
        do_i_like = Like.objects.filter(user=user, tweet_id=tweet_id).count()
        if do_i_like > 0:
            Like.objects.get(user=user, tweet_id=tweet_id).delete()
            return Response("", 204)
        raise PermissionDenied(detail="You haven't liked this tweet yet")
