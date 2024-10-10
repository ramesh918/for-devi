# users/serializers.py
from rest_framework import serializers as drf_serializers
from rest_framework_mongoengine import serializers
from .models import User
from django.contrib.auth.hashers import make_password

class RegisterSerializer(serializers.DocumentSerializer):
    password = drf_serializers.CharField(write_only=True, required=True, min_length=8)
    password2 = drf_serializers.CharField(write_only=True, required=True, label='Confirm Password')

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'password2', 'role')

    def validate(self, attrs):
        # Ensure passwords match
        if attrs['password'] != attrs['password2']:
            raise drf_serializers.ValidationError({"password": "Password fields didn't match."})
        
        # Ensure role is valid
        if attrs['role'] not in ('user', 'admin'):
            raise drf_serializers.ValidationError({"role": "Role must be either 'user' or 'admin'."})
        
        return attrs

    def create(self, validated_data):
        # Remove password2 from validated_data
        validated_data.pop('password2')
        password = validated_data.pop('password')
        
        # Create user with hashed password
        user = User(**validated_data)
        user.password = make_password(password)
        user.save()
        return user

class LoginSerializer(drf_serializers.Serializer):
    email = drf_serializers.EmailField(required=True)
    password = drf_serializers.CharField(write_only=True, required=True)

# class AssignmentSerializer(serializers.DocumentSerializer):
#     admin = drf_serializers.StringRelatedField()
#     user = drf_serializers.StringRelatedField()

#     class Meta:
#         model = Assignment
#         fields = ('id', 'user', 'task', 'admin', 'status', 'created_at', 'updated_at')

#     def to_representation(self, instance):
#         """Customize the output representation of the assignment."""
#         representation = super().to_representation(instance)
#         representation['admin'] = instance.admin.username  # Display admin's username
#         representation['user'] = instance.user.username    # Display user's username
#         return representation
