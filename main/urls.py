from django.urls import path, include
from rest_framework import routers

from .views import UserViewSet, AuthViewSet, EventViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'events', EventViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login', AuthViewSet.as_view()),
]
