from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class LoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="prueba", password="123")

    def test_login_success(self):
        self.client.get(reverse("signin"))
        response = self.client.post(reverse("signin"), {
            "username": "prueba",
            "password": "123",
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("task"))

    def test_login_failure(self):
        self.client.get(reverse("signin"))
        response = self.client.post(reverse("signin"), {
            "username": "wronguser",
            "password": "wrongpass",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nombre de usuario o contraseña incorrectos")

    def test_signup_success(self):
        self.client.get(reverse("signup"))
        response = self.client.post(reverse("signup"), {
            "username": "prueba",
            "password1": "123",
            "password2": "123"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Usuario ya existe")