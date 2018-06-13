
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from app.models import Tweet

class TweetSerializer(ModelSerializer):

    class Meta:
        fields = ["id", "body", "created", "author"]
        read_only_fields = ["author"]
        model = Tweet
