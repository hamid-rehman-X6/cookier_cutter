from rest_framework import serializers

from cookie_cutter.users.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    # password write only field (not returned in API)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ["id", "email", "name", "password", "is_staff"]

    def create(self, validated_data):
        """
        Create user with hashed password
        """
        password = validated_data.pop("password", None)

        # UserManager handles hashing the password
        user = User.objects.create(**validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

    def update(self, instance, validated_data):
        """
        Update user and handle password properly
        """
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance
