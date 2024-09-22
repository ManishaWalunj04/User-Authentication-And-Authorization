from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializers import UserSignupSerializer, UserLoginSerializer
from rest_framework.generics import ListAPIView
from django.db.models import Q
from .models import User
from .serializers import UserSearchSerializer
from django.contrib.auth import get_user_model
from rest_framework import generics
from django.contrib.auth import get_user_model
import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FriendRequest
from .serializers import FriendRequestSerializer

User = get_user_model()


class SignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            # logging.info("Success..................")
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSearchView(generics.ListAPIView):
    serializer_class = UserSearchSerializer

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword', None)

        if not keyword:
            return User.objects.none()  # Return an empty queryset if no keyword is provided

        # Search by email if the keyword matches exactly
        if '@' in keyword:
            return User.objects.filter(email__iexact=keyword)
        else:
            # Search by partial match in email (if keyword is part of the email)
            return User.objects.filter(email__icontains=keyword)


#############################Friend Request######################################


class SendFriendRequestView(APIView):
    def post(self, request):
        to_user_id = request.data.get('to_user')
        from_user = request.user

        # Create a new friend request
        friend_request = FriendRequest(from_user=from_user, to_user_id=to_user_id)
        friend_request.save()

        return Response({"message": "Friend request sent."}, status=status.HTTP_201_CREATED)


class AcceptFriendRequestView(APIView):
    def post(self, request, pk):
        try:
            friend_request = FriendRequest.objects.get(pk=pk, to_user=request.user)
            friend_request.accepted = True
            friend_request.save()
            return Response({"message": "Friend request accepted."}, status=status.HTTP_200_OK)
        except FriendRequest.DoesNotExist:
            return Response({"error": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND)


class RejectFriendRequestView(APIView):
    def post(self, request, pk):
        try:
            friend_request = FriendRequest.objects.get(pk=pk, to_user=request.user)
            friend_request.delete()
            return Response({"message": "Friend request rejected."}, status=status.HTTP_200_OK)
        except FriendRequest.DoesNotExist:
            return Response({"error": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND)
