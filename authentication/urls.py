from django.urls import path, include
from rest_framework import routers

from .views import RegisterUserView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'auth', RegisterUserView, basename='account')


urlpatterns = [
    path('', include(router.urls)),
]