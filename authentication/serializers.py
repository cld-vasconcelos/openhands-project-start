from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Role, UserRole, Session, MFADevice

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "is_email_verified",
            "profile_picture",
            "two_factor_enabled",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "is_email_verified", "created_at", "updated_at")


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "confirm_password")

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(**validated_data)
        return user


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ("id", "name")


class UserRoleSerializer(serializers.ModelSerializer):
    role = RoleSerializer()

    class Meta:
        model = UserRole
        fields = ("role", "created_at")


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ("id", "token", "created_at", "expires_at")
        read_only_fields = ("id", "created_at")


class MFADeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MFADevice
        fields = ("id", "secret_key", "enabled_at")
        read_only_fields = ("id", "enabled_at")
