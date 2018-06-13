from django.db import models
from django.contrib.auth.models import AbstractUser


# Likes?

class User(AbstractUser):
    pass


class Tweet(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=140, default="No tweet body provided")
    created = models.DateTimeField(auto_now_add=True)
    private = models.BooleanField(default=False)

    def likes(self):
        from app.serializers import LikeSerializer
        serialized_likes = LikeSerializer(self.like_set, many=True)
        return serialized_likes.data


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
