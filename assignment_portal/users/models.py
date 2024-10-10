# users/models.py

from mongoengine import Document, StringField, EmailField, DateTimeField, ValidationError
from datetime import datetime
import uuid

class User(Document):
    """
    Custom User model for MongoDB.
    """
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()), editable=False)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)  # Hashed password
    role = StringField(required=True, choices=['user', 'admin'])
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'users',
        'indexes': [
            {'fields': ['email'], 'unique': True},
        ]
    }

    @property
    def is_authenticated(self):
        """Always returns True. This is a way to tell if the user has been authenticated."""
        return True

    @property
    def is_active(self):
        """Always returns True. Override if you have inactive users."""
        return True

    @property
    def is_anonymous(self):
        """Always returns False. This is a way to tell if the user is anonymous."""
        return False

    def save(self, *args, **kwargs):
        """Automatically update the 'updated_at' field on each save."""
        self.updated_at = datetime.utcnow()
        return super(User, self).save(*args, **kwargs)
