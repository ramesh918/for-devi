# assignments/models.py

from mongoengine import Document, StringField, ReferenceField, DateTimeField
from datetime import datetime
from users.models import User
import uuid

class Assignment(Document):
    """
    Assignment model representing user submissions.
    """
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()), editable=False)
    user = ReferenceField(User, required=True, reverse_delete_rule=2)  # CASCADE
    task = StringField(required=True)
    admin = ReferenceField(User, required=True, reverse_delete_rule=2)  # Admin assigned to the task
    status = StringField(required=True, choices=['pending', 'accepted', 'rejected'], default='pending')
    remarks = StringField(required=False)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'assignments',
        'indexes': [
            {'fields': ['admin']},
        ]
    }

    def save(self, *args, **kwargs):
        # Automatically update the 'updated_at' field on each save
        self.updated_at = datetime.utcnow
        return super(Assignment, self).save(*args, **kwargs)