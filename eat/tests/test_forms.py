import os
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from eat.forms import RecipeForm


class TestRecipeForm(TestCase):

    def test_email_label(self):
        form = RecipeForm()
        self.assertTrue(form.fields['recipe_name'].label == "レシピ名")

    def test_site_label(self):
        form = RecipeForm()
        self.assertTrue(form.fields['site'].label == "参考サイト")

    def test_memo_label(self):
        form = RecipeForm()
        self.assertTrue(form.fields['memo'].label == "メモ")

    def test_photo_label(self):
        form = RecipeForm()
        self.assertTrue(form.fields['photo'].label == "写真")

    def test_ingredient_label(self):
        form = RecipeForm()
        self.assertTrue(form.fields['ingredient'].label == '材料')

    def test_type_label(self):
        form = RecipeForm()
        self.assertTrue(form.fields['type'].label == "種類")

    def test_piblic_label(self):
        form = RecipeForm()
        self.assertTrue(form.fields['public'].label == "公開")


    def test_form_is_valid(self):
        post_dict = {
            "recipe_name": "sample_recipe",
            "site": "recipe.url",
            "memo": "sample_memo",
            "ingredient": "sample_ingredient",
            "type": "ご飯",
            "user": "sample",
            "public": "公開",
            "quote": "無し",
        }
        fields_dict = {
            "photo": SimpleUploadedFile(
                name="smIMGL3647_TP_V.jpg",
                content=open(
                    os.path.join(
                        os.environ["HOME"],
                        'Desktop/picture/smIMGL3647_TP_V.jpg'), 'rb').read(),
                content_type="image/jpeg"
            )
        }
        form = RecipeForm(post_dict, fields_dict)
        self.assertTrue(form.is_valid())

    def test_site_is_valid(self):
        post_dict = {
            "recipe_name": "sample_recipe",
            "site": "recipe.url",
            "memo": "sample_memo",
            "ingredient": "sample_ingredient",
            "type": "ご飯",
            "user": "sample",
            "public": "公開",
            "quote": "無し",
        }
        fields_dict = {
            "photo": SimpleUploadedFile(
                name="smIMGL3647_TP_V.jpg",
                content=open(
                    os.path.join(
                        os.environ["HOME"],
                        'Desktop/picture/smIMGL3647_TP_V.jpg'), 'rb').read(),
                content_type="image/jpeg"
            )
        }
        form = RecipeForm(post_dict, fields_dict)
        self.assertTrue(form.is_valid())

    def test_memo_is_valid(self):
        post_dict = {
            "recipe_name": "sample_recipe",
            "site": "recipe.url",
            "memo": "",
            "ingredient": "sample_ingredient",
            "type": "ご飯",
            "user": "sample",
            "public": "公開",
            "quote": "無し",
        }
        fields_dict = {
            "photo": SimpleUploadedFile(
                name="smIMGL3647_TP_V.jpg",
                content=open(
                    os.path.join(
                        os.environ["HOME"],
                        'Desktop/picture/smIMGL3647_TP_V.jpg'), 'rb').read(),
                content_type="image/jpeg"
            )
        }
        form = RecipeForm(post_dict, fields_dict)
        self.assertTrue(form.is_valid())


    def test_photo_is_valid(self):
        post_dict = {
            "recipe_name": "sample_recipe",
            "site": "recipe.url",
            "memo": "sample_memo",
            "ingredient": "sample_ingredient",
            "type": "ご飯",
            "user": "sample",
            "public": "公開",
            "quote": "無し",
        }
        fields_dict = {
            "photo": ""
        }
        form = RecipeForm(post_dict, fields_dict)
        self.assertTrue(form.is_valid())

    def test_ingredient_max_length(self):
        post_dict = {
            "recipe_name": "sample_recipe",
            "site": "recipe.url",
            "memo": "sample_memo",
            "ingredient": "a" * 201,
            "type": "ご飯",
            "public": "公開",
            "quote": "無し",
        }
        fields_dict = {
            "photo": SimpleUploadedFile(
                name="smIMGL3647_TP_V.jpg",
                content=open(
                    os.path.join(
                        os.environ["HOME"],
                        'Desktop/picture/smIMGL3647_TP_V.jpg'), 'rb').read(),
                content_type="image/jpeg"
            )
        }
        form = RecipeForm(post_dict, fields_dict)
        self.assertFalse(form.is_valid())
