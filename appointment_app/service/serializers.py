from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class UserSerializers(serializers.ModelSerializer):
    """Serializers for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validate_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validate_data)


class AuthTokenSerializers(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            message = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(message, code='authentication')

        attrs['user'] = user

        return attrs
