from django.contrib.auth.models import User
from rest_framework.permissions import (
    SAFE_METHODS,
    IsAuthenticatedOrReadOnly,
    BasePermission
)

from .models import Tweet, Follow


class IsTweetAuthorOrReadOnly(IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, tweet: Tweet):
        if request.method in SAFE_METHODS:
            return True
        if tweet.author == request.user:
            return True
        return False


class FollowExist(BasePermission):

    def has_object_permission(self, request, view, obj: Follow):
        if request.method == "POST" and not Follow.objects.filter(
                follower=User.objects.get(username=view.kwargs["username"]),
                follows=request.user):
            return False

        return True
