from django.urls import path, include
from .views import RegistrationView, UserByIdView, UserInfoByUserView

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('registration/', RegistrationView.as_view(), name='rest_register'),
    path('user/<int:user_id>/', UserByIdView.as_view(), name='user_by_id'),
    path('userinfo/<int:user_id>/', UserInfoByUserView.as_view(), name='userinfo_by_user'),
]