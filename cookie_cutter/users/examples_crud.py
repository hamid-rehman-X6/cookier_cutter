"""
Example usage of User CRUD operations.

This script demonstrates how to use the User CRUD API in various ways:
1. Django ORM (direct model operations)
2. Django REST Framework API (HTTP requests)
3. Management commands
"""

# ============================================================================
# 1. Using Django ORM Directly
# ============================================================================

from cookie_cutter.users.models import User


def create_user_orm():
    """Create a user using Django ORM."""
    user = User.objects.create_user(
        email="orm@example.com",
        name="ORM User",
        password="ormpass123!",
    )
    print(f"Created user: {user.email}")
    return user


def read_users_orm():
    """Read/retrieve users using Django ORM."""
    # Get all users
    all_users = User.objects.all()
    print(f"Total users: {all_users.count()}")

    # Get specific user
    user = User.objects.get(email="orm@example.com")
    print(f"Retrieved user: {user.name}")

    # Filter users
    active_users = User.objects.filter(is_active=True)
    print(f"Active users: {active_users.count()}")

    return user


def update_user_orm():
    """Update a user using Django ORM."""
    user = User.objects.get(email="orm@example.com")
    user.name = "Updated ORM User"
    user.is_active = True
    user.save()
    print(f"Updated user: {user.name}")
    return user


def delete_user_orm():
    """Delete a user using Django ORM."""
    user = User.objects.get(email="orm@example.com")
    user_email = user.email
    user.delete()
    print(f"Deleted user: {user_email}")


# ============================================================================
# 2. Using REST Framework API (via test client)
# ============================================================================

from django.urls import reverse
from rest_framework.test import APIClient


class UserCRUDExample:
    """Example class showing REST API CRUD operations."""

    def __init__(self):
        self.client = APIClient()
        self.base_url = reverse("api:user-list")

    def create_user_api(self):
        """Create a user via REST API."""
        data = {
            "email": "api@example.com",
            "name": "API User",
            "password": "apipass123!",
        }
        response = self.client.post(self.base_url, data, format="json")
        if response.status_code == 201:
            print(f"Created user via API: {response.data['email']}")
            return response.data
        else:
            print(f"Error: {response.data}")
            return None

    def read_users_api(self):
        """Read/list users via REST API."""
        response = self.client.get(self.base_url)
        if response.status_code == 200:
            print(f"Retrieved {len(response.data)} users via API")
            return response.data
        else:
            print(f"Error: {response.status_code}")
            return None

    def read_specific_user_api(self, user_id):
        """Read a specific user via REST API."""
        url = reverse("api:user-detail", kwargs={"pk": user_id})
        response = self.client.get(url)
        if response.status_code == 200:
            print(f"Retrieved user via API: {response.data['email']}")
            return response.data
        else:
            print(f"Error: {response.status_code}")
            return None

    def update_user_api(self, user_id):
        """Update a user via REST API."""
        url = reverse("api:user-detail", kwargs={"pk": user_id})
        data = {
            "name": "Updated API User",
            "email": "api@example.com",
        }
        response = self.client.patch(url, data, format="json")
        if response.status_code == 200:
            print(f"Updated user via API: {response.data['name']}")
            return response.data
        else:
            print(f"Error: {response.data}")
            return None

    def delete_user_api(self, user_id):
        """Delete a user via REST API."""
        url = reverse("api:user-detail", kwargs={"pk": user_id})
        response = self.client.delete(url)
        if response.status_code == 204:
            print("User deleted via API")
            return True
        else:
            print(f"Error: {response.status_code}")
            return False

    def get_current_user_api(self):
        """Get current authenticated user via API."""
        # Note: This requires authentication
        url = reverse("api:user-me")
        response = self.client.get(url)
        if response.status_code == 200:
            print(f"Retrieved current user: {response.data['email']}")
            return response.data
        else:
            print(f"Error: {response.status_code}")
            return None


# ============================================================================
# 3. Using Management Command (Django)
# ============================================================================

"""
You can also create a custom management command:

# File: cookie_cutter/users/management/commands/crud_demo.py

from django.core.management.base import BaseCommand
from cookie_cutter.users.models import User


class Command(BaseCommand):
    help = 'Demonstrates CRUD operations on User model'

    def handle(self, *args, **options):
        # CREATE
        user = User.objects.create_user(
            email='command@example.com',
            name='Command User',
            password='cmdpass123!',
        )
        self.stdout.write(self.style.SUCCESS(f'Created: {user.email}'))

        # READ
        user = User.objects.get(email='command@example.com')
        self.stdout.write(f'Retrieved: {user.name}')

        # UPDATE
        user.name = 'Updated Command User'
        user.save()
        self.stdout.write(self.style.SUCCESS(f'Updated: {user.name}'))

        # DELETE
        user.delete()
        self.stdout.write(self.style.SUCCESS('Deleted user'))

# Run with: python manage.py crud_demo
"""

# ============================================================================
# 4. Usage Examples
# ============================================================================

if __name__ == "__main__":
    import os
    import django

    # Setup Django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
    django.setup()

    print("=" * 60)
    print("Django ORM CRUD Examples")
    print("=" * 60)

    # ORM Examples
    user = create_user_orm()
    read_users_orm()
    update_user_orm()
    delete_user_orm()

    print("\n" + "=" * 60)
    print("REST API CRUD Examples")
    print("=" * 60)

    # API Examples
    api = UserCRUDExample()

    # Create
    user_data = api.create_user_api()
    if user_data:
        user_id = user_data["id"]

        # Read
        api.read_users_api()
        api.read_specific_user_api(user_id)

        # Update
        api.update_user_api(user_id)

        # Delete
        api.delete_user_api(user_id)

    print("\n" + "=" * 60)
    print("Complete CRUD workflow examples executed!")
    print("=" * 60)
