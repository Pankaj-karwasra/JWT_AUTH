from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserModelSerializer, UserLoginSerializer, UserProfileSerializer, UserChangePasswrodSerailizer, SendPasswordEmailSerializer, UserPasswordResetSerializer
from rest_framework import status
from django.contrib.auth import authenticate
from app.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


# Function to generate JWT tokens for a user manually
def get_tokens_for_user(user):
    # Creating a refresh token for the user
    refresh = RefreshToken.for_user(user)

    # Returning the generated refresh and access tokens
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



# User Registration Endpoint
class UserRegistration(APIView):
    renderer_classes = [UserRenderer]
    
    def post(self, request, format=None):
        # Initialize the serializer with the request data
        serializer = UserModelSerializer(data=request.data)
        
        # Check if the data is valid
        if serializer.is_valid(raise_exception=True):
            # Save the user to the database
            user = serializer.save()
            # Generate tokens for the new user
            token = get_tokens_for_user(user)
            # Return the token and a success message
            return Response({'token': token, 'msg': 'Registration Success'}, status=status.HTTP_201_CREATED)
        
        # If serializer is invalid, return the error details
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Login Endpoint
class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    
    def post(self, request, format=None):
        # Initialize the serializer with the request data
        serializer = UserLoginSerializer(data=request.data)
        
        # Check if the data is valid
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            
            # Authenticate the user with the provided email and password
            user = authenticate(email=email, password=password)
            
            # If user exists, generate tokens and return them
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token, 'msg': 'Login Success'}, status=status.HTTP_200_OK)
            else:
                # If authentication fails, return an error message
                return Response({'error': {'non_field_errors': ['Email or password is not valid']}}, status=status.HTTP_400_BAD_REQUEST)
        
        # If serializer is invalid, return the error details
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Profile Endpoint
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view
    
    def get(self, request, format=None):
        # Serialize the current user's profile
        serializer = UserProfileSerializer(request.user)
        # Return the serialized data (user profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Change Password Endpoint
class UserChangePassword(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]  # Only authenticated users can change their password
    
    def post(self, request, format=None):
        # Initialize the serializer with the data and current user context
        serializer = UserChangePasswrodSerailizer(data=request.data, context={'user': request.user})
        
        # Check if the data is valid
        if serializer.is_valid(raise_exception=True):
            # Return a success message when the password is changed
            return Response({'msg': 'Password Changed Successfully'}, status=status.HTTP_200_OK)
        
        # If serializer is invalid, return the error details
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Send Password Reset Email Endpoint
class SendPasswordEmailView(APIView):
    renderer_classes = [UserRenderer]
    
    def post(self, request, format=None):
        # Initialize the serializer with the request data
        serializer = SendPasswordEmailSerializer(data=request.data)
        
        # Check if the data is valid
        if serializer.is_valid(raise_exception=True):
            # Return a success message indicating the email was sent
            return Response({'msg': 'Password Reset link send: Please check your email'}, status=status.HTTP_200_OK)
        
        # If serializer is invalid, return the error details
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Password Reset Endpoint
class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    
    def post(self, request, uid, token, format=None):
        # Initialize the serializer with the data, and pass the UID and token for validation
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid': uid, 'token': token})
        
        # Check if the data is valid
        if serializer.is_valid(raise_exception=True):
            # Return a success message when the password is reset successfully
            return Response({'msg': 'Password Reset Successfully'}, status=status.HTTP_200_OK)
        
        # If serializer is invalid, return the error details
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
