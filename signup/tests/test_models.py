from django.test import TestCase

from signup.models import User

class TestSignupModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
                                    username = "sample_name",
                                    password = "sample_pass",
                                    email = "sample@gmail.com",
                                    icon = "sample.img"
                                    )

    def test_email_name_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field("email").verbose_name
        self.assertEqual(field_label, "メールアドレス")

    def test_icon_upload_to(self):
        user = User.objects.get(id=1)
        upload_to = user._meta.get_field("icon").upload_to
        self.assertEqual(upload_to, "Media")
