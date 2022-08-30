from django.urls import path, include
from rest_framework import routers

from .views import UserViewSet, AuthViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login', AuthViewSet.as_view()),
]
