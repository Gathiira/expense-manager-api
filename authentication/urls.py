from django.urls import path, include
from rest_framework import routers

from .views import RegisterUserView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'account', RegisterUserView, basename='account')

urlpatterns = router.urls