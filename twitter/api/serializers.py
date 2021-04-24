from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Tweet, Follow


class UserWithUrlSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'last_name', 'first_name']
        extra_kwargs = {'url': {'lookup_field': 'username'}}


class UserWithoutUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'last_name', 'first_name']


class TweetSerializer(serializers.HyperlinkedModelSerializer):
    author = UserWithUrlSerializer(many=False, read_only=True)

    class Meta:
        model = Tweet
        fields = ['id', 'text', 'photo', 'created', 'author']


class FollowSerializer(serializers.HyperlinkedModelSerializer):
    #follows = serializers.SlugRelatedField('username')

    class Meta:
        model = Follow
        fields = []


class FollowsSerializer(serializers.HyperlinkedModelSerializer):
    follows = UserWithoutUrlSerializer(many=False, read_only=True)

    class Meta:
        model = Follow
        fields = ['follows', 'followed']


class FollowedSerializer(serializers.HyperlinkedModelSerializer):
    follower = UserWithoutUrlSerializer(many=False, read_only=True)

    class Meta:
        model = Follow
        fields = ['follower', 'followed']
