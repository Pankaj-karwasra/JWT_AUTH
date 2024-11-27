from rest_framework import serializers  # Importing serializers from DRF to create serialization classes
from app.models import User  # Import the User model from the app
from xml.dom import ValidationErr  # Import ValidationErr for handling validation errors
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError  # For handling string encoding/decoding
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode  # For handling URL-safe base64 encoding/decoding
from django.contrib.auth.tokens import PasswordResetTokenGenerator  # For generating password reset tokens
from app.utilies import Util  # Import the Util class for email-related functionality


# Register Serializer for User model
class UserModelSerializer(serializers.ModelSerializer):
    # Define additional password confirmation field
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User  # Use the User model for this serializer
        fields = ['email', 'name', 'password', 'password2', 'tc']  # Define the fields to be serialized
        extra_kwargs = {
            'password': {'write_only': True}  # Make the password field write-only (hidden in the response)
        }

    # Validate passwords (ensure password and password confirmation match)
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:  # Check if the passwords match
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return attrs
    
    # Create a new user instance after validation
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)  # Create a user using the validated data
    

# User login serializer
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)  # Email field for login

    class Meta:
        model = User  # Use the User model for this serializer
        fields = ['email', 'password']  # Fields required for login


# Profile Serializer to display user details
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Use the User model
        fields = ['id', 'email', 'name']  # Fields to be displayed in the profile


# Change password serializer
class UserChangePasswrodSerailizer(serializers.Serializer):
    # Fields for the new password and confirmation
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']  # Only these fields will be included in the request/response

    # Validate that passwords match and update the user's password
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')  # Access the user instance from context
        if password != password2:  # Ensure the passwords match
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        user.set_password(password)  # Set the new password for the user
        user.save()  # Save the updated user instance
        return attrs


# Send a password reset email to the user
class SendPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)  # The user's email address

    class Meta:
        fields = ['email']  # Only the email field is required

    # Validate the email and send a password reset link
    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():  # Check if the email exists in the database
            user = User.objects.get(email=email)  # Get the user object
            uid = urlsafe_base64_encode(force_bytes(user.id))  # Encode the user ID in base64 format
            print('Encoded UID', uid)
            token = PasswordResetTokenGenerator().make_token(user)  # Generate a password reset token
            link = 'http://localhost:3000/api/user/reset/' + uid + '/' + token  # Construct the password reset link
            print('Password Reset Link', link)

            # Send the reset email
            body = 'Click the following link to reset your password: ' + link
            data = {
                'subject': 'Reset Your Password',  # Subject of the email
                'body': body,  # Body content of the email
                'to_email': user.email  # Recipient email address
            }
            Util.send_email(data)  # Call the send_email method to send the email
            return attrs
        else:
            raise ValidationErr('You are not a Registered User')  # Raise an error if the email doesn't exist in the database


# Reset the user's password
class UserPasswordResetSerializer(serializers.Serializer):
    # Fields for the new password and confirmation
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']  # Only these fields are needed for resetting the password

    # Validate that passwords match and reset the password
    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')  # Get the user ID from the context
            token = self.context.get('token')  # Get the token from the context
            if password != password2:  # Ensure the passwords match
                raise serializers.ValidationError("Password and Confirm Password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))  # Decode the user ID from the base64-encoded string
            user = User.objects.get(id=id)  # Get the user object by ID
            if not PasswordResetTokenGenerator().check_token(user, token):  # Check if the token is valid
                raise ValidationErr('Token is not valid or expired')  # Raise an error if the token is invalid or expired
            user.set_password(password)  # Set the new password for the user
            user.save()  # Save the updated user instance
            
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            # Handle potential errors while decoding the UID
            PasswordResetTokenGenerator().check_token(user, token)  # Ensure the token is valid
            raise ValidationErr('Token is not valid or expired')  # Raise an error if token decoding fails
