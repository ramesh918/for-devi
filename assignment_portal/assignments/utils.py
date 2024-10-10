# assignments/utils.py

import jwt
from datetime import datetime, timedelta
from django.conf import settings

def generate_jwt(user):
    """
    Generates a JWT token for the given user.
    """
    payload = {
        'user_id': str(user.id),
        'exp': datetime.utcnow() + timedelta(hours=24),  # Token expires in 24 hours
        'iat': datetime.utcnow(),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token