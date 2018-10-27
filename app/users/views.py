from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import mixins
from app.users.serializers import UserSerializer, RegisterSerializer


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  GenericViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class RegisterUserView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            token = serializer.save()
            return Response(data=token, status=status.HTTP_201_CREATED)
