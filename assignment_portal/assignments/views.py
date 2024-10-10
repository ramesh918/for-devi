# assignments/views.py

from rest_framework import generics, status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .serializers import AssignmentSerializer, CreateAssignmentSerializer
from .models import Assignment
from users.models import User
from rest_framework.permissions import IsAuthenticated  # Import DRF's IsAuthenticated
from .authentication import CustomJWTAuthentication  # Import your custom authentication class
from .permissions import IsAdmin
from mongoengine.errors import DoesNotExist

class UploadAssignmentView(generics.CreateAPIView):
    """
    Endpoint for users to upload assignments.
    """
    serializer_class = CreateAssignmentSerializer
    # authentication_classes = [CustomJWTAuthentication]  # Set custom authentication
    # permission_classes = [IsAuthenticated]  # Use DRF's permission class

    def perform_create(self, serializer):
        # Associate the assignment with the authenticated user
        serializer.save(user=self.request.user)

class AdminAssignmentListView(generics.ListAPIView):
    """
    Endpoint for admins to view their assigned assignments.
    """
    serializer_class = AssignmentSerializer
    authentication_classes = [CustomJWTAuthentication]  # Set custom authentication
    permission_classes = [IsAuthenticated, IsAdmin]  # Use DRF's permission classes

    def get_queryset(self):
        # Get the assignments assigned to the authenticated admin user
        admin_user = self.request.user
        return Assignment.objects(admin=admin_user)

@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])  # Set custom authentication for function-based views
@permission_classes([IsAuthenticated, IsAdmin])  # Use DRF's permission classes
def accept_assignment(request, pk):
    """
    Endpoint for admins to accept an assignment.
    """
    try:
        # Retrieve the assignment for the given primary key (pk)
        assignment = Assignment.objects.get(id=pk, admin=request.user)
    except DoesNotExist:
        return Response({"error": "Assignment not found."}, status=status.HTTP_404_NOT_FOUND)

    if assignment.status != 'pending':
        return Response({"error": f"Assignment already {assignment.status}."}, status=status.HTTP_400_BAD_REQUEST)

    # Update assignment status to accepted
    assignment.status = 'accepted'
    assignment.save()
    return Response({"message": "Assignment accepted."}, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])  # Set custom authentication for function-based views
@permission_classes([IsAuthenticated, IsAdmin])  # Use DRF's permission classes
def reject_assignment(request, pk):
    """
    Endpoint for admins to reject an assignment.
    """
    try:
        # Retrieve the assignment for the given primary key (pk)
        assignment = Assignment.objects.get(id=pk, admin=request.user)
    except DoesNotExist:
        return Response({"error": "Assignment not found."}, status=status.HTTP_404_NOT_FOUND)

    if assignment.status != 'pending':
        return Response({"error": f"Assignment already {assignment.status}."}, status=status.HTTP_400_BAD_REQUEST)

    # Update assignment status to rejected
    assignment.status = 'rejected'
    assignment.save()
    return Response({"message": "Assignment rejected."}, status=status.HTTP_200_OK)
