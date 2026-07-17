from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from task.models import Task


class AddTaskTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.client.login(username="testuser", password="testpass123")
        session = self.client.session
        session.save()
        self.session_token = session.session_key

    def test_create_task_success(self):
        self.client.get(reverse("create_task"))
        response = self.client.post(reverse("create_task"), {
            "title": "Mi nueva tarea",
            "description": "Descripcion de la tarea",
            "priority": 1,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("task"))
        self.assertTrue(Task.objects.filter(title="Mi nueva tarea").exists())

    def test_create_task_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("create_task"))
        self.assertRedirects(response, f"{reverse('signin')}?next={reverse('create_task')}")

    def test_create_task_invalid_data(self):
        response = self.client.post(reverse("create_task"), {
            "title": "",
            "description": "",
            "priority": 1,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Por favor ingrese datos válidos")

    def test_create_task_default_priority(self):
        response = self.client.post(reverse("create_task"), {
            "title": "Tarea sin prioridad",
            "description": "Test",
            "priority": 0,
        })
        self.assertEqual(response.status_code, 302)
        task = Task.objects.get(title="Tarea sin prioridad")
        self.assertEqual(task.priority, 0)

    def test_task_assigned_to_logged_user(self):
        response = self.client.post(reverse("create_task"), {
            "title": "Tarea de testuser",
            "description": "Asignacion",
            "priority": 2,
        })
        self.assertEqual(response.status_code, 302)
        task = Task.objects.get(title="Tarea de testuser")
        self.assertEqual(task.user, self.user)