from rest_framework import serializers

from cookie_cutter.users.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    """Serializer for User model with full CRUD operations."""

    password = serializers.CharField(
        write_only=True,
        required=False,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "name",
            "password",
            "is_active",
            "is_staff",
            "date_joined",
            "url",
        ]
        read_only_fields = ["id", "date_joined"]
        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
            "email": {"required": True},
        }

    def create(self, validated_data):
        """Create a new user instance with hashed password."""
        password = validated_data.pop("password", None)
        user = User.objects.create_user(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        """Update user instance, handling password separately."""
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
