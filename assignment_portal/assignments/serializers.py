# assignments/serializers.py

from rest_framework import serializers
from .models import Assignment  # Ensure this imports your MongoEngine Assignment model
from users.models import User  # Ensure this imports your User model
import uuid

class AssignmentSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    task = serializers.CharField(required=True)
    admin = serializers.StringRelatedField()  # Assuming `admin` is a ReferenceField to the User model
    user = serializers.StringRelatedField()    # Assuming there's a user who created the assignment
    status = serializers.CharField(read_only=True)  # Read-only field
    created_at = serializers.DateTimeField(read_only=True)  # Read-only field
    updated_at = serializers.DateTimeField(read_only=True)  # Read-only field

    def to_representation(self, instance):
        """Customize the output representation of the assignment."""
        representation = super().to_representation(instance)
        # Customize how the admin and user are displayed
        representation['admin'] = f"{instance.admin.first_name} {instance.admin.last_name}"
        representation['user'] = f"{instance.user.first_name} {instance.user.last_name}"
        return representation

class CreateAssignmentSerializer(serializers.Serializer):
    task = serializers.CharField(required=True)
    admin = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='admin'))  # Ensure admin is an admin user

    def validate_admin(self, value):
        if value.role != 'admin':
            raise serializers.ValidationError("Assigned user must be an admin.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        # Assuming 'admin' is a ReferenceField to the User model
        assignment = Assignment(
            task=validated_data['task'],
            admin=validated_data['admin'],
            user=user  # Associate the assignment with the authenticated user
        )
        assignment.save()  # Save the assignment to the database
        return assignment
