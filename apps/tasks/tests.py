from rest_framework.test import APITestCase
from django.urls import reverse
from apps.accounts.models import User
from apps.tasks.models import Task

class TaskAPITest(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            email="admin@test.com",
            password="Admin@123",
            role="ADMIN",
            full_name="Admin User"
        )

        self.client.force_authenticate(user=self.admin)

    def test_create_task(self):
        data = {
            "title": "Test Task",
            "description": "Testing task creation",
            "assigned_to": self.admin.id
        }

        response = self.client.post("/api/tasks/", data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.objects.count(), 1)
