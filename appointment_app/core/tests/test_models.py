from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):
    def test_create_user_with_email_successfull(self):
        """Test creating a new user with email is successfull"""

        email = "alfonsorodrigo12@gmail.com"
        password = "Test1"
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""

        email = "alfonsorodrigo12@GMAIL.COM"
        user = get_user_model().objects.create_user(email, "Test2")
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "Test3")

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser("alfonso@gmail.com", "Test4")

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
