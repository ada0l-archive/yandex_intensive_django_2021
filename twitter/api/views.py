from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, mixins

from .models import Tweet, Follow
from .permissions import IsTweetAuthorOrReadOnly, FollowExist
from .serializers import (
    UserWithUrlSerializer,
    TweetSerializer,
    FollowSerializer,
    FollowsSerializer,
    FollowedSerializer
)


class UsersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('-date_joined', 'username')
    serializer_class = UserWithUrlSerializer
    lookup_field = 'username'


class TweetsViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all().order_by('-created')
    serializer_class = TweetSerializer
    permission_classes = [
        IsTweetAuthorOrReadOnly
    ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserTweetsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tweet.objects
    serializer_class = TweetSerializer

    def get_queryset(self):
        return self.queryset.filter(
            author__username=self.kwargs['parent_lookup_username']
        )


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    GenericViewSet):
    queryset = Follow.objects
    serializer_class = FollowSerializer
    permission_classes = [
        FollowExist
    ]
    lookup_field = 'username'

    def get_lookup_field(self):
        return self.kwargs[self.lookup_field]

    def perform_create(self, serializer):
        serializer.save(
            follows=User.objects.get(username=self.get_lookup_field()),
            follower=self.request.user
        )

    def get_object(self):
        return Follow.objects.get(
            follows=User.objects.get(username=self.get_lookup_field()),
            follower=self.request.user
        )


class FeedViewSet(mixins.ListModelMixin,
                  GenericViewSet):
    queryset = Tweet.objects
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticated]

    def filter_queryset(self, queryset):
        return queryset.filter(author__follower__follower=self.request.user)


class FollowsListViewSet(mixins.ListModelMixin,
                         GenericViewSet):
    queryset = Follow.objects
    serializer_class = FollowsSerializer
    lookup_field = 'username'

    def get_user(self):
        return User.objects.get(username=self.kwargs["parent_lookup_username"])

    def filter_queryset(self, queryset):
        return queryset.filter(follower=self.get_user())


class FollowedListViewSet(FollowsListViewSet):
    serializer_class = FollowedSerializer

    def filter_queryset(self, queryset):
        return queryset.filter(follows=self.get_user())
