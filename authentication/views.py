from django.conf import settings
from django.urls import reverse

from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site

import jwt

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import RegisterUserSerializer
from .models import User
from .helper import Helper

class RegisterUserView(viewsets.ViewSet):
    serializer_class = RegisterUserSerializer

    @swagger_auto_schema(manual_parameters=[])
    @action(methods=['POST'], detail=False, url_path="register-user", url_name="register_user")
    def register_user(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        serializer.is_valid(raise_exception = True) # run validate method
        serializer.save()   # run create method

        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token


        current_site = get_current_site(request).domain
        relative_link = reverse('account-verify_email')

        absolute_url = 'http://' + current_site + relative_link + '?token='+ str(token)
        email_body = 'Hi ' + user.username + "\nClick on the link below to verify your email\n\n" + absolute_url
        data = {'email_body':email_body, 'to_email':user.email, 'email_subject':"verify your email"}

        Helper.send_email(data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)




    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description = 'pass in the token to verify'
        , type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    @action(methods=['GET'], detail=False, url_path="verify-email", url_name="verify_email")
    def verify_email(self,reguest):
        token = reguest.GET.get('token')
        try:
            payload= jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'detail':"Email successfully activated"}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as e:
            print(e)
            return Response({'error':"ACTIVATION link expired"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError as e:
            print(e)
            return Response({'error':"INVALID token"}, status=status.HTTP_400_BAD_REQUEST)