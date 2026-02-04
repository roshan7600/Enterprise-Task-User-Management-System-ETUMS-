from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token
from rest_framework import serializers
from .models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims to the token
        token['email'] = user.email
        token['full_name'] = user.full_name
        token['role'] = user.role
        token['is_active'] = user.is_active
        token['is_staff'] = user.is_staff
        
        return token
    
    def validate(self, attrs):
        # SimpleJWT expects "username" internally
        attrs["username"] = attrs.get("email")
        data = super().validate(attrs)
        
        # Add user information to response
        user = self.user
        data['user'] = {
            'id': user.id,
            'email': user.email,
            'full_name': user.full_name,
            'role': user.role,
            'is_active': user.is_active,
            'is_staff': user.is_staff
        }
        
        return data
# 👤 User List / Create Serializer (Admin APIs)
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "full_name", "role"]



# Adding a New user via API

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "full_name", "password", "role"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
