from django.contrib import admin
from django.urls import include, path
from rest_framework_extensions.routers import ExtendedDefaultRouter

from twitter.api.router import SwitchDetailRouter
from twitter.api.views import (
    UsersViewSet,
    TweetsViewSet,
    UserTweetsViewSet,
    FollowViewSet,
    FeedViewSet,
    FollowsListViewSet,
    FollowedListViewSet
)

router = ExtendedDefaultRouter()
router.register(r'tweets', TweetsViewSet)
router.register(r'feed', FeedViewSet)

user_route = router.register(r'users', UsersViewSet)
user_route.register(r'tweets', UserTweetsViewSet, 'user-tweets', ['username'])
user_route.register(r'follows', FollowsListViewSet, 'user-follows', ['username'])
user_route.register(r'followed', FollowedListViewSet, 'user-followed', ['username'])

switch_router = SwitchDetailRouter()
switch_router.register(r'follow', FollowViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include(switch_router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
