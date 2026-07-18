from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from task.models import Task


class UpdateTaskTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.client.login(username="testuser", password="testpass123")
        session = self.client.session
        session.save()
        self.session_token = session.session_key
        self.task = Task.objects.create(
            title="Tarea original",
            description="Descripcion original",
            priority=0,
            user=self.user,
        )

    def test_update_task_success(self):
        response = self.client.post(
            reverse("task_detail", args=[self.task.id]),
            {"title": "Tarea actualizada", "description": "Nueva descripcion", "priority": 2},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("task"))
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Tarea actualizada")
        self.assertEqual(self.task.description, "Nueva descripcion")
        self.assertEqual(self.task.priority, 2)

    def test_update_task_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("task_detail", args=[self.task.id]))
        self.assertRedirects(
            response, f"{reverse('signin')}?next={reverse('task_detail', args=[self.task.id])}"
        )

    def test_update_task_not_owner(self):
        other_user = User.objects.create_user(username="other", password="other123")
        other_task = Task.objects.create(
            title="Tarea de otro", description="Ajena", priority=1, user=other_user
        )
        response = self.client.get(reverse("task_detail", args=[other_task.id]))
        self.assertEqual(response.status_code, 404)

    def test_update_task_invalid_data(self):
        response = self.client.post(
            reverse("task_detail", args=[self.task.id]),
            {"title": "", "description": "", "priority": 1},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")

    def test_update_task_get_form(self):
        response = self.client.get(reverse("task_detail", args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tarea original")
        self.assertContains(response, "Descripcion original")

    def test_complete_task(self):
        response = self.client.post(reverse("complete_task", args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("task"))
        self.task.refresh_from_db()
        self.assertIsNotNone(self.task.date_completed)

    def test_uncomplete_task(self):
        self.task.date_completed = __import__("django").utils.timezone.now()
        self.task.save()
        response = self.client.post(reverse("complete_task", args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertIsNone(self.task.date_completed)

    def test_complete_task_not_owner(self):
        other_user = User.objects.create_user(username="other2", password="other123")
        other_task = Task.objects.create(
            title="Tarea de otro", description="Ajena", priority=1, user=other_user
        )
        response = self.client.post(reverse("complete_task", args=[other_task.id]))
        self.assertEqual(response.status_code, 404)
