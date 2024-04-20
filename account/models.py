from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userinfo')
    avatar_url = models.URLField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=(('male', 'Male'), ('female', 'Female'), ('other', 'Other')), blank=True, null=True)
    bio = models.TextField(blank=True, null=True)




