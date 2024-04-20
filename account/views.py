from rest_framework.response import Response
from rest_framework import status,viewsets, permissions
from dj_rest_auth.registration.views import RegisterView
from chat.models import Setting
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import UserDetailsSerializer, UserInfoSerializer
from rest_framework import viewsets
from .models import UserInfo
User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailsSerializer


class UserByIdView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        return get_object_or_404(User, id=user_id)


class RegistrationView(RegisterView):
    def create(self, request, *args, **kwargs):
        try:
            open_registration = Setting.objects.get(name='open_registration').value == 'True'
        except Setting.DoesNotExist:
            open_registration = True

        if open_registration is False:
            return Response({'detail': 'Registration is not yet open.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = self.get_response_data(user)

        if data:
            response = Response(
                data,
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        else:
            response = Response(status=status.HTTP_204_NO_CONTENT, headers=headers)

        return response


class UserInfoByUserView(generics.RetrieveAPIView):
    serializer_class = UserInfoSerializer

    def get_queryset(self):
        """
        仅允许用户访问自己的额外信息
        """
        user_id = self.kwargs['user_id']
        return UserInfo.objects.filter(user__id=user_id)

    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.get()
        return obj