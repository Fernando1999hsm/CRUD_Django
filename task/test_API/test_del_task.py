from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from task.models import Task


class DeleteTaskTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.client.login(username="testuser", password="testpass123")
        session = self.client.session
        session.save()
        self.session_token = session.session_key
        self.task = Task.objects.create(
            title="Tarea a eliminar",
            description="Se va a borrar",
            priority=1,
            user=self.user,
        )

    def test_delete_task_success(self):
        response = self.client.post(reverse("delete_task", args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("task"))
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_delete_task_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("delete_task", args=[self.task.id]))
        self.assertRedirects(
            response, f"{reverse('signin')}?next={reverse('delete_task', args=[self.task.id])}"
        )

    def test_delete_task_not_owner(self):
        other_user = User.objects.create_user(username="other", password="other123")
        other_task = Task.objects.create(
            title="Tarea ajena", description="No me pertenece", priority=0, user=other_user
        )
        response = self.client.post(reverse("delete_task", args=[other_task.id]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Task.objects.filter(id=other_task.id).exists())

    def test_delete_nonexistent_task(self):
        response = self.client.post(reverse("delete_task", args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_delete_task_get_request(self):
        response = self.client.get(reverse("delete_task", args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("task"))
        self.assertTrue(Task.objects.filter(id=self.task.id).exists())
