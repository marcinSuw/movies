from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from rest_framework_jwt.serializers import JSONWebTokenSerializer, authenticate
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()


class UserLoginRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'password',
        )

    email = serializers.EmailField(max_length=128, write_only=True,
                                   validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(max_length=128, write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'date_joined',

        )
        extra_kwargs = {
            'password': {'write_only': True},
            'is_staff': {'read_only': True},
            'is_active': {'read_only': True},
        }


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8, write_only=True,)

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["email"],
            validated_data["password"])
        if user:
            payload = jwt_payload_handler(user)
            return {
                'token': jwt_encode_handler(payload)
            }
        return user

    class Meta:
        fields = [
            'email',
            'password',
        ]


class CustomJWTSerializer(JSONWebTokenSerializer):
    username_field = 'email'

    def validate(self, attrs):

        password = attrs.get("password")
        user = User.objects.filter(
            email=attrs.get("email")).first()
        if user is not None:
            credentials = {
                'email': user.email,
                'password': password
            }
            if all(credentials.values()):
                user = authenticate(**credentials)
                if user:
                    if not user.is_active:
                        msg = 'User account is disabled.'
                        raise serializers.ValidationError(msg)
                    payload = jwt_payload_handler(user)
                    return {
                        'token': jwt_encode_handler(payload),
                        'user': user
                    }
                else:
                    msg = 'Unable to log in with provided credentials.'
                    raise serializers.ValidationError(msg)
            else:
                msg = 'Must include "{username_field}" and "password".'
                msg = msg.format(username_field=self.username_field)
                raise serializers.ValidationError(msg)
        else:
            msg = 'Account with this email/username does not exists'
            raise serializers.ValidationError(msg)
