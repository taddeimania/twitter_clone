
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from app.models import Tweet, Like


class TweetSerializer(ModelSerializer):

    likes = serializers.ListField(read_only=True)

    class Meta:
        fields = "__all__"
        read_only_fields = ["author", "likes"]
        model = Tweet


class LikeSerializer(ModelSerializer):

    class Meta:
        fields = "__all__"
        model = Like
