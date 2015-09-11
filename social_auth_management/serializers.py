from social.apps.django_app.default.models import UserSocialAuth
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.Serializer):

    class Meta:
        model = User
