"""Tests for User API CRUD operations."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from cookie_cutter.users.models import User

from .factories import UserFactory

if TYPE_CHECKING:
    from django.test.client import Client


@pytest.mark.django_db
class TestUserCreateAPI(TestCase):
    """Test User Create operation via API."""

    def setUp(self):
        """Set up test client."""
        self.client = APIClient()
        self.create_url = reverse("api:user-list")

    def test_create_user_success(self):
        """Test successful user creation."""
        data = {
            "email": "newuser@example.com",
            "name": "New User",
            "password": "testpass123!",
        }
        response = self.client.post(self.create_url, data, format="json")
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["email"] == "newuser@example.com"
        assert response.data["name"] == "New User"
        assert User.objects.filter(email="newuser@example.com").exists()

    def test_create_user_missing_email(self):
        """Test user creation fails without email."""
        data = {
            "name": "New User",
            "password": "testpass123!",
        }
        response = self.client.post(self.create_url, data, format="json")
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data

    def test_create_user_duplicate_email(self):
        """Test user creation fails with duplicate email."""
        UserFactory(email="existing@example.com")
        data = {
            "email": "existing@example.com",
            "name": "Another User",
            "password": "testpass123!",
        }
        response = self.client.post(self.create_url, data, format="json")
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserReadAPI(TestCase):
    """Test User Read operations via API."""

    def setUp(self):
        """Set up test client and test data."""
        self.client = APIClient()
        self.user = UserFactory(email="testuser@example.com", name="Test User")
        self.list_url = reverse("api:user-list")
        self.detail_url = reverse("api:user-detail", kwargs={"pk": self.user.pk})

    def test_list_users(self):
        """Test listing all users."""
        UserFactory.create_batch(3)
        response = self.client.get(self.list_url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_retrieve_user_success(self):
        """Test retrieving a single user."""
        response = self.client.get(self.detail_url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == "testuser@example.com"
        assert response.data["name"] == "Test User"

    def test_retrieve_user_not_found(self):
        """Test retrieving non-existent user."""
        url = reverse("api:user-detail", kwargs={"pk": 99999})
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_current_user_endpoint(self):
        """Test /me endpoint for current user."""
        self.client.force_authenticate(user=self.user)
        url = reverse("api:user-me")
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == "testuser@example.com"


@pytest.mark.django_db
class TestUserUpdateAPI(TestCase):
    """Test User Update operation via API."""

    def setUp(self):
        """Set up test client and test data."""
        self.client = APIClient()
        self.user = UserFactory(email="testuser@example.com", name="Test User")
        self.detail_url = reverse("api:user-detail", kwargs={"pk": self.user.pk})

    def test_update_user_success(self):
        """Test successful user update."""
        data = {
            "name": "Updated User",
            "email": "testuser@example.com",
        }
        response = self.client.put(self.detail_url, data, format="json")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Updated User"
        
        self.user.refresh_from_db()
        assert self.user.name == "Updated User"

    def test_partial_update_user_success(self):
        """Test successful partial user update."""
        data = {"name": "Partially Updated"}
        response = self.client.patch(self.detail_url, data, format="json")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Partially Updated"
        assert response.data["email"] == "testuser@example.com"

    def test_update_user_password(self):
        """Test updating user password."""
        data = {
            "email": "testuser@example.com",
            "name": "Test User",
            "password": "newpassword123!",
        }
        response = self.client.patch(self.detail_url, data, format="json")
        
        assert response.status_code == status.HTTP_200_OK
        
        self.user.refresh_from_db()
        assert self.user.check_password("newpassword123!")

    def test_update_nonexistent_user(self):
        """Test updating non-existent user."""
        url = reverse("api:user-detail", kwargs={"pk": 99999})
        data = {"name": "Updated User"}
        response = self.client.patch(url, data, format="json")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUserDeleteAPI(TestCase):
    """Test User Delete operation via API."""

    def setUp(self):
        """Set up test client and test data."""
        self.client = APIClient()
        self.user = UserFactory(email="testuser@example.com", name="Test User")

    def test_delete_user_success(self):
        """Test successful user deletion."""
        detail_url = reverse("api:user-detail", kwargs={"pk": self.user.pk})
        response = self.client.delete(detail_url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not User.objects.filter(pk=self.user.pk).exists()

    def test_delete_nonexistent_user(self):
        """Test deleting non-existent user."""
        url = reverse("api:user-detail", kwargs={"pk": 99999})
        response = self.client.delete(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestUserCRUDAPIIntegration(APITestCase):
    """Integration tests for complete CRUD workflow."""

    def setUp(self):
        """Set up test client."""
        self.client = APIClient()
        self.list_url = reverse("api:user-list")

    def test_complete_crud_workflow(self):
        """Test complete CRUD workflow: Create, Read, Update, Delete."""
        # CREATE
        create_data = {
            "email": "workflow@example.com",
            "name": "Workflow User",
            "password": "workflowpass123!",
        }
        create_response = self.client.post(self.list_url, create_data, format="json")
        assert create_response.status_code == status.HTTP_201_CREATED
        user_id = create_response.data["id"]
        user_url = reverse("api:user-detail", kwargs={"pk": user_id})

        # READ
        read_response = self.client.get(user_url)
        assert read_response.status_code == status.HTTP_200_OK
        assert read_response.data["email"] == "workflow@example.com"

        # UPDATE
        update_data = {
            "name": "Updated Workflow User",
            "email": "workflow@example.com",
        }
        update_response = self.client.patch(user_url, update_data, format="json")
        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.data["name"] == "Updated Workflow User"

        # DELETE
        delete_response = self.client.delete(user_url)
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify deletion
        verify_response = self.client.get(user_url)
        assert verify_response.status_code == status.HTTP_404_NOT_FOUND
