from django.test import TestCase
import os
from django.core.files.uploadedfile import SimpleUploadedFile

from signup.forms import CustomUserCreationForm, CustomUserChangeForm, CustomUpdateForm

class TestCustomUserCreationForm(TestCase):

    def test_email_label(self):
        form = CustomUserCreationForm()
        self.assertTrue(form.fields['email'].label == "メールアドレス")

    def test_form_is_valid(self):
        data = {
            "username": "sample",
            "email": "sample@gmail.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        form = CustomUserCreationForm(data)
        self.assertTrue(form.is_valid())

class TestCustomUserChangeForm(TestCase):

    def test_email_label(self):
        form = CustomUserChangeForm()
        self.assertTrue(form.fields["email"].label == "メールアドレス")

    def test_icon_label(self):
        form = CustomUserChangeForm()
        self.assertTrue(form.fields["icon"].label == "アイコン")

    def test_form_is_valid(self):
        post_dict = {
            "username": "sample",
            "email": "sample@gmail.com",
        }
        files_dict = {
            "icon": SimpleUploadedFile(
                name = "illustration-2541681_1280.jpg",
                content = open(os.path.join(os.environ["HOME"], 'Desktop/picture/illustration-2541681_1280.jpg'), 'rb').read(),
                content_type = "image/jpeg"
            )
        }
        form = CustomUserChangeForm(post_dict, files_dict)
        self.assertTrue(form.is_valid())

    def test_icon_is_valid(self):
        post_dict = {
            "username": "sample",
            "email": "sample@gmail.com",
        }
        files_dict = {
            "icon": ""
        }
        form = CustomUserChangeForm(post_dict, files_dict)
        self.assertTrue(form.is_valid())
