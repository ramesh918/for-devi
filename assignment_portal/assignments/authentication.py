# assignments/authentication.py

import jwt
from rest_framework import authentication, exceptions
from django.conf import settings
from users.models import User  # Ensure this import points to your User model

class CustomJWTAuthentication(authentication.BaseAuthentication):
    """
    Custom JWT authentication using MongoEngine.
    """

    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header or auth_header[0].lower() != b'bearer':
            return None  # No authentication provided

        if len(auth_header) == 1:
            raise exceptions.AuthenticationFailed('Invalid token header. No credentials provided.')
        elif len(auth_header) > 2:
            raise exceptions.AuthenticationFailed('Invalid token header. Token string should not contain spaces.')

        try:
            token = auth_header[1].decode('utf-8')
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired.')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token.')

        user_id = payload.get('user_id')

        if not user_id:
            raise exceptions.AuthenticationFailed('Invalid token payload.')

        try:
            user = User.objects.get(id=user_id)  # Make sure to use your MongoEngine query
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No user matching this token was found.')

        return (user, token)  # Return the user object
