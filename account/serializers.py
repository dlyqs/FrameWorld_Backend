from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import UserInfo

# Get the UserModel
UserModel = get_user_model()


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email')
        read_only_fields = ('email',)


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['user', 'avatar_url', 'gender', 'bio']
        read_only_fields = ('user',)