from io import BytesIO

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from PIL import Image

from .models import Category, Post


def _tiny_png_upload(name="t.png"):
    buf = BytesIO()
    Image.new("RGB", (8, 8), (40, 80, 120)).save(buf, format="PNG")
    buf.seek(0)
    return SimpleUploadedFile(name, buf.read(), content_type="image/png")


class BlogPublicPagesTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_ok(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)

    def test_login_page_has_fields(self):
        r = self.client.get("/login/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'name="username"')
        self.assertContains(r, 'name="password"')
        self.assertContains(r, "input-control")

    def test_register_page_has_fields(self):
        r = self.client.get("/register/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'name="username"')
        self.assertContains(r, "input-control")


class BlogAuthFlowTests(TestCase):
    def test_register_login_logout(self):
        c = Client()
        r = c.post(
            "/register/",
            {
                "username": "testuser",
                "email": "",
                "password1": "ComplexPass!234",
                "password2": "ComplexPass!234",
            },
            follow=True,
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(User.objects.filter(username="testuser").exists())

        c.logout()
        r = c.post(
            "/login/",
            {"username": "testuser", "password": "ComplexPass!234"},
            follow=True,
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.context["user"].is_authenticated)

        r = c.post("/logout/", follow=True)
        self.assertEqual(r.status_code, 200)


class BlogPostVisibilityTests(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name="T", slug="t")
        self.author = User.objects.create_user("a", password="p")
        self.post = Post.objects.create(
            title="X",
            content="c",
            image=_tiny_png_upload(),
            category=self.cat,
            author=self.author,
            is_approved=False,
        )

    def test_unapproved_hidden_from_home(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertNotContains(r, "X")

    def test_unapproved_visible_to_author(self):
        self.client.login(username="a", password="p")
        r = self.client.get(self.post.get_absolute_url())
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "X")
