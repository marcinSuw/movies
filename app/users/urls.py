from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework_jwt.views import ObtainJSONWebToken

from app.users.views import UserViewSet, RegisterUserView
from app.users.serializers import CustomJWTSerializer

router = DefaultRouter()
router.register('users', UserViewSet, base_name='users')

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', ObtainJSONWebToken.as_view(serializer_class=CustomJWTSerializer), name='login'),
    path('', include(router.urls))
]
