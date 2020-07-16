from django.test import TestCase
from django.urls import reverse
from django.test.client import Client
from django.db.models import Q

from eat.models import Recipe
from signup.models import User

class OnlyUserRequiredMixin(TestCase):
    def setUp(self):
        client = Client()
        self.user = User.objects.create_user("sample", "sample@gmail.com", "pass")
        recipe = Recipe.objects.create(
            recipe_name="sample_recipe_name",
            site="sample.url",
            memo="sample_memo",
            photo="sample.img",
            ingredient="sample_ingredient",
            type="ご飯",
            date="2018-10-25 14:30:59",
            user=self.user,
            )

    def test_user_login_url(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get("/eat/update/1/")
        self.assertEqual(response.status_code, 200)

    def test_user_login_name(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(reverse('eat:update', kwargs={'pk': 1}),)
        self.assertEqual(response.status_code, 200)

    def test_user_not_login_url(self):
        response = self.client.get("/eat/update/1/")
        self.assertEqual(response.status_code, 403)

    def test_user_not_login_name(self):
        response = self.client.get(reverse('eat:update', kwargs={'pk': 1}),)
        self.assertEqual(response.status_code, 403)


#いいね機能のテスト
class TestGood(TestCase):
    def setUp(self):
        client = Client()
        self.user = User.objects.create_user("sample", "sample@gmail.com", "pass")

#投稿に、いいねしていないとき　url
    def test_recipe_object_none_good_name(self):
        self.client.login(username="sample", password="pass")
        recipe = Recipe.objects.create(
            recipe_name="sample_recipe_name",
            site="sample.url",
            memo="sample_memo",
            photo="sample.img",
            ingredient="sample_ingredient",
            type="ご飯",
            date="2018-10-25 14:30:59",
            user=self.user,
            )
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(str(recipe.good_user.all()), "<QuerySet []>")
        response = self.client.get(
            reverse('eat:good', kwargs={'pk': 1}),
            HTTP_REFERER=str(reverse('eat:find')),
            follow=True
            )
        self.assertEqual(response.status_code, 200)
        recipe = Recipe.objects.get(id=1)
        users = User.objects.filter(username='sample')
        self.assertEqual(list(recipe.good_user.all()), list(users))

#投稿に、いいねしていないとき　name
    def test_recipe_object_none_good_url(self):
        self.client.login(username="sample", password="pass")
        recipe = Recipe.objects.create(
            recipe_name="sample_recipe_name",
            site="sample.url",
            memo="sample_memo",
            photo="sample.img",
            ingredient="sample_ingredient",
            type="ご飯",
            date="2018-10-25 14:30:59",
            user=self.user,
            )
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(str(list(recipe.good_user.all())), "[]")
        response = self.client.get(
            '/eat/1/',
            HTTP_REFERER=str(reverse('eat:find')),
            follow=True
            )
        self.assertEqual(response.status_code, 200)
        recipe = Recipe.objects.get(id=1)
        users = User.objects.filter(username='sample')
        self.assertEqual(str(list(recipe.good_user.all())), "[<User: sample>]")

#投稿に、いいねしているとき　name
    def test_recipe_object_good_name(self):
        self.client.login(username="sample", password="pass")
        recipe = Recipe.objects.create(
            recipe_name="sample_recipe_name",
            site="sample.url",
            memo="sample_memo",
            photo="sample.img",
            ingredient="sample_ingredient",
            type="ご飯",
            date="2018-10-25 14:30:59",
            user=self.user,
            )
        recipe.good_user.add(self.user)
        recipe = Recipe.objects.get(id=1)
        users = User.objects.filter(username='sample')
        self.assertEqual(list(recipe.good_user.all()), list(users))
        response = self.client.get(
            reverse('eat:good', kwargs={'pk': 1}),
            HTTP_REFERER=str(reverse('eat:find')),
            follow=True
            )
        self.assertEqual(response.status_code, 200)
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(str(list(recipe.good_user.all())), "[]")

#ログアウトしているとき
    def test_recipe_object_good_name_not_login(self):
        response = self.client.get(
            reverse('eat:good', kwargs={'pk': 1}),
            HTTP_REFERER=str(reverse('eat:find')),
            follow=True
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")


class TestEatGoodUsersListView(TestCase):
    def setUp(self):
        client = Client()
        self.user = User.objects.create_user("sample", "sample@gmail.com", "pass")
        user2 = User.objects.create_user("sample2", "sample2@gmail.com", "pass2")
        user3 = User.objects.create_user("sample3", "sample3@gmail.com", "pass3")
        self.user.follow.add(user2)
        #self.userのオブジェクト
        user_recipe1 = Recipe.objects.create(
            recipe_name="recipe_name1",
            ingredient="ingredient1",
            type="ご飯",
            user=self.user,
            public="公開"
            )
        user_recipe2 = Recipe.objects.create(
            recipe_name="recipe_name2",
            ingredient="ingredient2",
            type="ご飯",
            user=self.user,
            public="非公開"
            )
        user_recipe3 = Recipe.objects.create(
            recipe_name="recipe_name3",
            ingredient="ingredient2",
            type="ご飯",
            user=self.user,
            public="友達のみ"
            )
        #フォローしている人の投稿
        user2_recipe4 = Recipe.objects.create(
            recipe_name="recipe_name4",
            ingredient="ingredient4",
            type="ご飯",
            user=user2,
            public="公開"
            )
        user2_recipe5 = Recipe.objects.create(
            recipe_name="recipe_name5",
            ingredient="ingredient5",
            type="ご飯",
            user=user2,
            public="非公開"
            )
        user2_recipe6 = Recipe.objects.create(
            recipe_name="recipe_name6",
            ingredient="ingredient6",
            type="ご飯",
            user=user2,
            public="友達のみ"
            )

#いいねしていない場合 urlでのアクセス
    def test_url_none_good(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get('/eat/list/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_good_users_list.html")
        self.assertEqual(str(response.context["object_list"]), '<QuerySet []>')
        self.assertEqual(response.context["recipe_count"], 3)
        self.assertEqual(response.context["users"], self.user)
        self.assertEqual(response.context["follower_count"], 0)

#いいねしていない場合 nameでのアクセス
    def test_name_none_good(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(reverse("eat:good_users_list", kwargs={'users_id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_good_users_list.html")
        self.assertEqual(str(response.context["object_list"]), '<QuerySet []>')
        self.assertEqual(response.context["recipe_count"], 3)
        self.assertEqual(response.context["users"], self.user)
        self.assertEqual(response.context["follower_count"], 0)

#フォローしているユーザーがいる場合
    def test_name_follow_good(self):
        self.client.login(username="sample", password="pass")
        user2_objects = Recipe.objects.filter(user=2)
        #user2の投稿をいいねする
        for user2_object in user2_objects:
            user2_object.good_user.add(self.user)
        response = self.client.get(
            reverse("eat:good_users_list", kwargs={'users_id': 1})
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_good_users_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name6>, <Recipe: recipe_name4>]"
            )
        self.assertEqual(response.context["recipe_count"], 3)
        self.assertEqual(response.context["users"], self.user)
        self.assertEqual(response.context["follower_count"], 0)

#ログインしていない場合
    def test_name_not_login(self):
        user2_objects = Recipe.objects.filter(user=2)
        #user2の投稿をいいねする
        for user2_object in user2_objects:
            user2_object.good_user.add(self.user)
        response = self.client.get(
            reverse("eat:good_users_list", kwargs={'users_id': 1})
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_good_users_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            '[<Recipe: recipe_name4>]'
            )
        self.assertEqual(response.context["recipe_count"], 3)
        self.assertEqual(response.context["users"], self.user)
        self.assertEqual(response.context["follower_count"], 0)

#並び替え　order=old
    def test_url_order_old(self):
        self.client.login(username="sample", password="pass")
        user2_objects = Recipe.objects.filter(user=2)
        #user2の投稿をいいねする
        for user2_object in user2_objects:
            user2_object.good_user.add(self.user)
        response = self.client.get("/eat/list/1/?order=old")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name4>, <Recipe: recipe_name6>]"
            )

#並び替え　order=new
    def test_name_order_new(self):
        self.client.login(username="sample", password="pass")
        user2_objects = Recipe.objects.filter(user=2)
        #user2の投稿をいいねする
        for user2_object in user2_objects:
            user2_object.good_user.add(self.user)
        response = self.client.get(
            reverse("eat:good_users_list", kwargs={'users_id': 1}),
            {"order": "new"}
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name6>, <Recipe: recipe_name4>]"
            )

#検索　serch=ご飯
    def test_name_search_word(self):
        self.client.login(username="sample", password="pass")
        user2_objects = Recipe.objects.filter(user=2)
        #user2の投稿をいいねする
        for user2_object in user2_objects:
            user2_object.good_user.add(self.user)
        response = self.client.get(
            reverse("eat:good_users_list", kwargs={'users_id': 1}),
            {"search": "ご飯"}
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_good_users_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name6>, <Recipe: recipe_name4>]"
            )

#検索　serch=ご飯, order=new
    def test_name_search_word_and_order_new(self):
        self.client.login(username="sample", password="pass")
        user2_objects = Recipe.objects.filter(user=2)
        #user2の投稿をいいねする
        for user2_object in user2_objects:
            user2_object.good_user.add(self.user)
        response = self.client.get(
            reverse("eat:good_users_list", kwargs={'users_id': 1}),
            {'order':'new', 'search':'ご飯'}
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_good_users_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name6>, <Recipe: recipe_name4>]"
            )

#検索　serch=ご飯, order=old
    def test_name_search_word_and_order_old(self):
        self.client.login(username="sample", password="pass")
        user2_objects = Recipe.objects.filter(user=2)
        #user2の投稿をいいねする
        for user2_object in user2_objects:
            user2_object.good_user.add(self.user)
        response = self.client.get(
            reverse("eat:good_users_list", kwargs={'users_id': 1}),
            {'order':'old', 'search':'ご飯'}
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_good_users_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name4>, <Recipe: recipe_name6>]"
            )

class TestEatListView(TestCase):
    def setUp(self):
        client = Client()
        self.user = User.objects.create_user("sample", "sample@gmail.com", "pass")
        #self.userのオブジェクト
        user_recipe1 = Recipe.objects.create(
            recipe_name="recipe_name1",
            ingredient="ingredient1",
            type="ご飯",
            user=self.user,
            public="公開"
            )
        user_recipe2 = Recipe.objects.create(
            recipe_name="recipe_name2",
            ingredient="ingredient2",
            type="ご飯",
            user=self.user,
            public="非公開"
            )
        user_recipe3 = Recipe.objects.create(
            recipe_name="recipe_name3",
            ingredient="ingredient2",
            type="おかず",
            user=self.user,
            public="友達のみ"
            )

#ログインしていない場合
    def test_name_not_login(self):
        response = self.client.get(reverse('eat:index'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

#いいねしていない場合 urlでのアクセス
    def test_url(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get('/eat/index/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name3>, <Recipe: recipe_name2>, <Recipe: recipe_name1>]"
            )
        self.assertEqual(response.context["recipe_count"], 3)
        self.assertEqual(response.context["users"], self.user)
        self.assertEqual(response.context["follower_count"], 0)

#いいねしていない場合 nameでのアクセス
    def test_name(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(reverse('eat:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name3>, <Recipe: recipe_name2>, <Recipe: recipe_name1>]"
            )
        self.assertEqual(response.context["recipe_count"], 3)
        self.assertEqual(response.context["users"], self.user)
        self.assertEqual(response.context["follower_count"], 0)

#並び替え　order=old
    def test_name_order_old(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(
            reverse('eat:index'),
            {'order':'old'}
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name1>, <Recipe: recipe_name2>, <Recipe: recipe_name3>]"
            )

#並び替え　order=new
    def test_name_order_new(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(
            reverse('eat:index'),
            {'order':'new'}
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name3>, <Recipe: recipe_name2>, <Recipe: recipe_name1>]"
            )

#検索　serch=ご飯
    def test_name_search_word(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(
            reverse('eat:index'),
            {'search':'ご飯'}
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name2>, <Recipe: recipe_name1>]"
            )

#検索　serch=ご飯, order=new
    def test_name_search_word_and_order_new(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(
            reverse('eat:index'),
            {'order':'new', 'search':'ご飯'}
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name2>, <Recipe: recipe_name1>]"
            )

#検索　serch=ご飯, order=old
    def test_name_search_word_and_order_old(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(
            reverse('eat:index'),
            {'order':'old', 'search':'ご飯'}
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name1>, <Recipe: recipe_name2>]"
            )

#deletes
    def test_url_deletes(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(reverse('eat:index'))
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name3>, <Recipe: recipe_name2>, <Recipe: recipe_name1>]"
            )
        self.assertEqual(response.status_code, 200)
        delete = "recipe_name2"
        response = self.client.post("/eat/index/?deletes=deletes", {'delete': 1}, follow=True)
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name3>, <Recipe: recipe_name2>]"
            )

class TestEatTimeLineListView(TestCase):
    def setUp(self):
        client = Client()
        self.user = User.objects.create_user("sample", "sample@gmail.com", "pass")
        user2 = User.objects.create_user("sample2", "sample2@gmail.com", "pass2")
        user3 = User.objects.create_user("sample3", "sample3@gmail.com", "pass3")
        self.user.follow.add(user2)
        #self.userのオブジェクト
        user_recipe1 = Recipe.objects.create(
            recipe_name="recipe_name1",
            ingredient="ingredient1",
            type="ご飯",
            user=self.user,
            public="公開"
            )
        user_recipe2 = Recipe.objects.create(
            recipe_name="recipe_name2",
            ingredient="ingredient2",
            type="ご飯",
            user=self.user,
            public="非公開"
            )
        user_recipe3 = Recipe.objects.create(
            recipe_name="recipe_name3",
            ingredient="ingredient2",
            type="ご飯",
            user=self.user,
            public="友達のみ"
            )
        #フォローしている人の投稿
        user2_recipe4 = Recipe.objects.create(
            recipe_name="recipe_name4",
            ingredient="ingredient4",
            type="ご飯",
            user=user2,
            public="公開"
            )
        user2_recipe5 = Recipe.objects.create(
            recipe_name="recipe_name5",
            ingredient="ingredient5",
            type="ご飯",
            user=user2,
            public="非公開"
            )
        user2_recipe6 = Recipe.objects.create(
            recipe_name="recipe_name6",
            ingredient="ingredient6",
            type="スープ",
            user=user2,
            public="友達のみ"
            )
        #フォローしていない人の投稿
        user3_recipe7 = Recipe.objects.create(
            recipe_name="recipe_name7",
            ingredient="ingredient7",
            type="ご飯",
            user=user3,
            public="公開"
            )
        user3_recipe8 = Recipe.objects.create(
            recipe_name="recipe_name8",
            ingredient="ingredient8",
            type="ご飯",
            user=user3,
            public="非公開"
            )
        user2_recipe9 = Recipe.objects.create(
            recipe_name="recipe_name9",
            ingredient="ingredient9",
            type="ご飯",
            user=user3,
            public="友達のみ"
            )

#ログインしていない場合
    def test_name_not_login(self):
        response = self.client.get(reverse('eat:timeline'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

#検索ワードがない場合
    def test_url(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get('/eat/timeline/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_timeline_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name6>, <Recipe: recipe_name4>, <Recipe: recipe_name3>, <Recipe: recipe_name1>]"
            )

#検索ワードがない場合 url
    def test_url(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get('/eat/timeline/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_timeline_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name6>, <Recipe: recipe_name4>, <Recipe: recipe_name3>, <Recipe: recipe_name1>]"
            )

#検索ワードがない場合　name
    def test_name(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(reverse('eat:timeline'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_timeline_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name6>, <Recipe: recipe_name4>, <Recipe: recipe_name3>, <Recipe: recipe_name1>]"
            )

#並び替え　order=old
    def test_name_order_old(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(
            reverse('eat:timeline'),
            {'order':'old'}
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_timeline_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name1>, <Recipe: recipe_name3>, <Recipe: recipe_name4>, <Recipe: recipe_name6>]"
            )

#並び替え　order=new
    def test_name_order_new(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(
            reverse('eat:timeline'),
            {'order':'new'}
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_timeline_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name6>, <Recipe: recipe_name4>, <Recipe: recipe_name3>, <Recipe: recipe_name1>]"
            )

#検索　serch=ご飯
    def test_name_search_word(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(
            reverse('eat:timeline'),
            {'search':'ご飯'}
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_timeline_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name4>, <Recipe: recipe_name3>, <Recipe: recipe_name1>]"
            )

#検索　serch=ご飯 order=new
    def test_name_search_word_order_new(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(
            reverse('eat:timeline'),
            {'search':'ご飯', "order": "new"}
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_timeline_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name4>, <Recipe: recipe_name3>, <Recipe: recipe_name1>]"
            )

#検索　serch=ご飯 order=old
    def test_name_search_word_order_old(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(
            reverse('eat:timeline'),
            {'search':'ご飯', "order": "old"}
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_timeline_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name1>, <Recipe: recipe_name3>, <Recipe: recipe_name4>]"
            )

class TesEatUsersListView(TestCase):
    def setUp(self):
        client = Client()
        self.user = User.objects.create_user("sample", "sample@gmail.com", "pass")
        user2 = User.objects.create_user("sample2", "sample2@gmail.com", "pass2")
        user3 = User.objects.create_user("sample3", "sample3@gmail.com", "pass3")
        self.user.follow.add(user2)
        #self.userのオブジェクト
        user_recipe1 = Recipe.objects.create(
            recipe_name="recipe_name1",
            ingredient="ingredient1",
            type="ご飯",
            user=self.user,
            public="公開"
            )
        user_recipe2 = Recipe.objects.create(
            recipe_name="recipe_name2",
            ingredient="ingredient2",
            type="ご飯",
            user=self.user,
            public="非公開"
            )
        user_recipe3 = Recipe.objects.create(
            recipe_name="recipe_name3",
            ingredient="ingredient2",
            type="ご飯",
            user=self.user,
            public="友達のみ"
            )
        #フォローしている人の投稿
        user2_recipe4 = Recipe.objects.create(
            recipe_name="recipe_name4",
            ingredient="ingredient4",
            type="ご飯",
            user=user2,
            public="公開"
            )
        user2_recipe5 = Recipe.objects.create(
            recipe_name="recipe_name5",
            ingredient="ingredient5",
            type="ご飯",
            user=user2,
            public="非公開"
            )
        user2_recipe6 = Recipe.objects.create(
            recipe_name="recipe_name6",
            ingredient="ingredient6",
            type="スープ",
            user=user2,
            public="友達のみ"
            )
        #フォローしていない人の投稿
        user3_recipe7 = Recipe.objects.create(
            recipe_name="recipe_name7",
            ingredient="ingredient7",
            type="ご飯",
            user=user3,
            public="公開"
            )
        user3_recipe8 = Recipe.objects.create(
            recipe_name="recipe_name8",
            ingredient="ingredient8",
            type="ご飯",
            user=user3,
            public="非公開"
            )
        user2_recipe9 = Recipe.objects.create(
            recipe_name="recipe_name9",
            ingredient="ingredient9",
            type="ご飯",
            user=user3,
            public="友達のみ"
            )
        user2_recipe10 = Recipe.objects.create(
            recipe_name="recipe_name10",
            ingredient="ingredient10",
            type="ご飯",
            user=user3,
            public="公開"
            )
        user2_recipe11 = Recipe.objects.create(
            recipe_name="recipe_name11",
            ingredient="ingredient11",
            type="スープ",
            user=user3,
            public="公開"
            )

#検索ワードがない場合 フォローしているユーザー
    def test_url_follow_user2(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get('/eat/users/2', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name6>, <Recipe: recipe_name4>]"
            )
        self.assertEqual(response.context["recipe_count"], 3)
        self.assertEqual(str(response.context["users"]), "sample2")
        self.assertEqual(response.context["follower_count"], 1)

#検索ワードがない場合 フォローしているユーザー
    def test_name_follow_user2(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(
            reverse("eat:users", kwargs={'users_id': 2}),
            follow=True
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name6>, <Recipe: recipe_name4>]"
            )
        self.assertEqual(response.context["recipe_count"], 3)
        self.assertEqual(str(response.context["users"]), "sample2")
        self.assertEqual(response.context["follower_count"], 1)

#並び替え　order=old フォローしているユーザー
    def test_name_follow_user2_order_old(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(
            reverse("eat:users", kwargs={'users_id': 2}),
            {'order':'old'}
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name4>, <Recipe: recipe_name6>]"
            )

#並び替え　order=old フォローしているユーザー
    def test_name_follow_user2_order_new(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(
            reverse("eat:users", kwargs={'users_id': 2}),
            {'order':'new'}
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name6>, <Recipe: recipe_name4>]"
            )

#検索ワードがない場合 フォローしていないユーザー
    def test_name_follow_user3(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(
            reverse("eat:users", kwargs={'users_id': 3}),
            follow=True
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name11>, <Recipe: recipe_name10>, <Recipe: recipe_name7>]"
            )
        self.assertEqual(response.context["recipe_count"], 5)
        self.assertEqual(str(response.context["users"]), "sample3")
        self.assertEqual(response.context["follower_count"], 0)

#検索ワード フォローしていないユーザー
    def test_name_follow_user3_serch(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(
            reverse("eat:users", kwargs={'users_id': 3}),
            {"search": "ご飯"},
            follow=True
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name10>, <Recipe: recipe_name7>]"
            )

#検索ワード order=new フォローしていないユーザー
    def test_name_follow_user3_serch_order_new(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(
            reverse("eat:users", kwargs={'users_id': 3}),
            {"search": "ご飯", "order":"new"},
            follow=True
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name10>, <Recipe: recipe_name7>]"
            )

#検索ワード order=new フォローしていないユーザー
    def test_name_follow_user3_serch_order_old(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(
            reverse("eat:users", kwargs={'users_id': 3}),
            {"search": "ご飯", "order":"old"},
            follow=True
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name7>, <Recipe: recipe_name10>]"
            )

    def test_name_my_page(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(
            reverse("eat:users", kwargs={'users_id': 1}),
            follow=True
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name3>, <Recipe: recipe_name2>, <Recipe: recipe_name1>]"
            )
        self.assertEqual(response.context["recipe_count"], 3)
        self.assertEqual(response.context["users"], self.user)
        self.assertEqual(response.context["follower_count"], 0)


    def test_name_not_login(self):
        response = self.client.get(
            reverse("eat:users", kwargs={'users_id': 1}),
            follow=True
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name1>]"
            )

class TestEatFindListView(TestCase):
    def setUp(self):
        client = Client()
        self.user = User.objects.create_user("sample", "sample@gmail.com", "pass")
        user2 = User.objects.create_user("sample2", "sample2@gmail.com", "pass2")
        user3 = User.objects.create_user("sample3", "sample3@gmail.com", "pass3")
        self.user.follow.add(user2)
        #self.userのオブジェクト
        user_recipe1 = Recipe.objects.create(
            recipe_name="recipe_name1",
            ingredient="ingredient1",
            type="ご飯",
            user=self.user,
            public="公開"
            )
        user_recipe2 = Recipe.objects.create(
            recipe_name="recipe_name2",
            ingredient="ingredient2",
            type="ご飯",
            user=self.user,
            public="非公開"
            )
        user_recipe3 = Recipe.objects.create(
            recipe_name="recipe_name3",
            ingredient="ingredient2",
            type="ご飯",
            user=self.user,
            public="友達のみ"
            )
        #フォローしている人の投稿
        user2_recipe4 = Recipe.objects.create(
            recipe_name="recipe_name4",
            ingredient="ingredient4",
            type="ご飯",
            user=user2,
            public="公開"
            )
        user2_recipe5 = Recipe.objects.create(
            recipe_name="recipe_name5",
            ingredient="ingredient5",
            type="ご飯",
            user=user2,
            public="非公開"
            )
        user2_recipe6 = Recipe.objects.create(
            recipe_name="recipe_name6",
            ingredient="ingredient6",
            type="スープ",
            user=user2,
            public="友達のみ"
            )
        #フォローしていない人の投稿
        user3_recipe7 = Recipe.objects.create(
            recipe_name="recipe_name7",
            ingredient="ingredient7",
            type="ご飯",
            user=user3,
            public="公開"
            )
        user3_recipe8 = Recipe.objects.create(
            recipe_name="recipe_name8",
            ingredient="ingredient8",
            type="ご飯",
            user=user3,
            public="非公開"
            )
        user2_recipe9 = Recipe.objects.create(
            recipe_name="recipe_name9",
            ingredient="ingredient9",
            type="ご飯",
            user=user3,
            public="友達のみ"
            )
        user2_recipe10 = Recipe.objects.create(
            recipe_name="recipe_name10",
            ingredient="ingredient10",
            type="ご飯",
            user=user3,
            public="公開"
            )
        user2_recipe11 = Recipe.objects.create(
            recipe_name="recipe_name11",
            ingredient="ingredient11",
            type="スープ",
            user=user3,
            public="公開"
            )
#検索ワード無し　name
    def test_name(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(reverse("eat:find"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_find_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name11>, <Recipe: recipe_name10>, <Recipe: recipe_name7>, <Recipe: recipe_name6>, <Recipe: recipe_name4>, <Recipe: recipe_name3>, <Recipe: recipe_name2>, <Recipe: recipe_name1>]"
            )

    def test_url(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get("/eat/find/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_find_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name11>, <Recipe: recipe_name10>, <Recipe: recipe_name7>, <Recipe: recipe_name6>, <Recipe: recipe_name4>, <Recipe: recipe_name3>, <Recipe: recipe_name2>, <Recipe: recipe_name1>]"
            )

#order=new
    def test_name_new(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(
            reverse("eat:find"),
            {"order": "new"}
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_find_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name11>, <Recipe: recipe_name10>, <Recipe: recipe_name7>, <Recipe: recipe_name6>, <Recipe: recipe_name4>, <Recipe: recipe_name3>, <Recipe: recipe_name2>, <Recipe: recipe_name1>]"
            )

#order=old
    def test_name_old(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(
            reverse("eat:find"),
            {"order": "old"}
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_find_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name1>, <Recipe: recipe_name2>, <Recipe: recipe_name3>, <Recipe: recipe_name4>, <Recipe: recipe_name6>, <Recipe: recipe_name7>, <Recipe: recipe_name10>, <Recipe: recipe_name11>]"
            )

#search
    def test_name_search(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(
            reverse("eat:find"),
            {"search": "ご飯"}
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_find_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name10>, <Recipe: recipe_name7>, <Recipe: recipe_name4>, <Recipe: recipe_name3>, <Recipe: recipe_name2>, <Recipe: recipe_name1>]"
            )

#search order=new
    def test_name_search_oeder_new(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(
            reverse("eat:find"),
            {"search": "ご飯", "order": "new"}
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_find_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name10>, <Recipe: recipe_name7>, <Recipe: recipe_name4>, <Recipe: recipe_name3>, <Recipe: recipe_name2>, <Recipe: recipe_name1>]"
            )

#search order=old
    def test_name_search_oeder_old(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(
            reverse("eat:find"),
            {"search": "ご飯", "order": "old"}
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_find_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name1>, <Recipe: recipe_name2>, <Recipe: recipe_name3>, <Recipe: recipe_name4>, <Recipe: recipe_name7>, <Recipe: recipe_name10>]"
            )

#ログインしていないとき
    def test_not_login(self):
        response = self.client.get(reverse("eat:find"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_find_list.html")
        self.assertEqual(
            str(list(response.context["object_list"])),
            "[<Recipe: recipe_name11>, <Recipe: recipe_name10>, <Recipe: recipe_name7>, <Recipe: recipe_name4>, <Recipe: recipe_name1>]"
            )

class TestEatDetailView(TestCase):

    def setUp(self):
        client = Client()
        self.user = User.objects.create_user("sample", "sample@gmail.com", "pass")
        user2 = User.objects.create_user("sample2", "sample2@gmail.com", "pass2")
        self.user.follow.add(user2)
        user_recipe1 = Recipe.objects.create(
            recipe_name="recipe_name1",
            ingredient="ingredient1",
            type="ご飯",
            user=self.user,
            public="公開"
            )
        user_recipe2 = Recipe.objects.create(
            recipe_name="recipe_name2",
            ingredient="ingredient2",
            type="ご飯",
            user=user2,
            public="公開",
            quote_recipe=user_recipe1
            )

#quote_recipe 有り　name
    def test_name(self):
        response = self.client.get(reverse("eat:detail", kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_detail.html")
        self.assertEqual(str(list(response.context["object_list"])), '[<Recipe: recipe_name2>]')

#quote_recipe 有り　url
    def test_url(self):
        response = self.client.get("/eat/detail/1/")
        self.assertTemplateUsed(response, "eat/recipe_detail.html")
        self.assertEqual(str(list(response.context["object_list"])), '[<Recipe: recipe_name2>]')

#quote_recipe 無し name
    def test_url_none_quote_recipe(self):
        response = self.client.get(reverse("eat:detail", kwargs={'pk':2}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_detail.html")
        self.assertEqual(str(list(response.context["object_list"])), '[]')

class TestEatQuoteDetailView(TestCase):
    def setUp(self):
        client = Client()
        self.user = User.objects.create_user("sample", "sample@gmail.com", "pass")
        user2 = User.objects.create_user("sample2", "sample2@gmail.com", "pass2")
        self.user.follow.add(user2)
        user_recipe1 = Recipe.objects.create(
            recipe_name="recipe_name1",
            ingredient="ingredient1",
            type="ご飯",
            user=self.user,
            public="公開"
            )
        user_recipe2 = Recipe.objects.create(
            recipe_name="recipe_name2",
            ingredient="ingredient2",
            type="ご飯",
            user=user2,
            public="公開",
            quote_recipe=user_recipe1,
            quote="有り"
            )
        user_recipe3 = Recipe.objects.create(
            recipe_name="recipe_name3",
            ingredient="ingredient3",
            type="ご飯",
            user=user2,
            public="公開",
            )
        user_recipe3.quote_user.add(self.user)

#作成者とログインユーザーが一致しない場合 作成ページへ移動
    def test_name(self):
        #ユーザー２でログイン
        self.client.login(username="sample2", password="pass2")
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(str(list(recipe.quote_user.all())), "[]")
        response = self.client.get(reverse("eat:quote_detail", kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/quote_recipe.html")
        self.assertEqual(str(list(recipe.quote_user.all())), "[]")
        self.assertEqual(str(response.context["object"]), 'recipe_name1')

#作成者とログインユーザーが一致しない場合 作成ページへ移動
    def test_url(self):
        #ユーザー２でログイン
        self.client.login(username="sample2", password="pass2")
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(str(list(recipe.quote_user.all())), "[]")
        response = self.client.get("/eat/detail/quote/1/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/quote_recipe.html")
        self.assertEqual(str(list(recipe.quote_user.all())), "[]")
        self.assertEqual(str(response.context["object"]), 'recipe_name1')

    def test_name_quote(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(
            reverse('eat:quote_detail', kwargs={'pk': 2}),
            HTTP_REFERER=str(reverse('signup:top')),
            follow=True
            )
        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]), "参考cookに参考cookは作成できません")

    def test_name_quote_user(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(
            reverse('eat:quote_detail', kwargs={'pk': 3}),
            HTTP_REFERER=str(reverse('signup:top')),
            follow=True
            )
        msg = """このレシピの参考cookは作成済みです。レシピは<a href='/eat/delete/3/'> こちら </a>から削除できます"""
        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]), msg)

    def test_name_create_user_equal_login_user(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(reverse("eat:quote_detail", kwargs={'pk': 1}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup/top.html")

    def test_name_not_login(self):
        response = self.client.get(reverse("eat:quote_detail", kwargs={'pk': 1}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

class TestEatCreateView(TestCase):
    def setUp(self):
        client = Client()
        self.user = User.objects.create_user("sample", "sample@gmail.com", "pass")

    def test_name(self):
        self.client.login(username="sample", password="pass")
        data = {
            "recipe_name": "recipe_name",
            "ingredient": "ingredient",
            "type": "スープ",
            "user": self.user,
            "public": "公開"
            }
        response = self.client.post(reverse('eat:create'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('eat:index'))


    def test_url(self):
        self.client.login(username="sample", password="pass")
        data = {
            "recipe_name": "recipe_name",
            "ingredient": "ingredient",
            "type": "スープ",
            "user": self.user,
            "public": "公開"
            }
        response = self.client.post("/eat/create/", data=data)
        self.assertEqual(response.status_code, 302)

    def test_name_success_messages(self):
        self.client.login(username="sample", password="pass")
        data = {
            "recipe_name": "recipe_name",
            "ingredient": "ingredient",
            "type": "スープ",
            "user": self.user,
            "public": "公開"
            }
        response = self.client.post(reverse('eat:create'), data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('eat:index'))
        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]), "保存しました")

    def test_name_error_messages(self):
        self.client.login(username="sample", password="pass")
        data = {
            "recipe_name": "recipe_name",
            "ingredient": "",
            "type": "スープ",
            "user": self.user,
            "public": "公開"
            }
        response = self.client.post(reverse('eat:create'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_create_form.html")
        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]), "保存に失敗しました")

class TestEatQuoteCreateView(TestCase):
    def setUp(self):
        client = Client()
        self.user = User.objects.create_user("sample", "sample@gmail.com", "pass")
        user2 = User.objects.create_user("sample2", "sample2@gmail.com", "pass2")
        self.user.follow.add(user2)
        user1_recipe1 = Recipe.objects.create(
            recipe_name="recipe_name1",
            ingredient="ingredient1",
            type="ご飯",
            user=self.user,
            public="公開"
            )
        user1_recipe2 = Recipe.objects.create(
            recipe_name="recipe_name2",
            ingredient="ingredient2",
            type="ご飯",
            user=self.user,
            public="公開"
            )
        #user2のuser_recipe2に対する参考cook
        user2_recipe3 = Recipe.objects.create(
            recipe_name="recipe_name3",
            ingredient="ingredient3",
            type="ご飯",
            user=user2,
            quote_recipe=user1_recipe2,
            quote="有り",
            public="公開",
            )
        user1_recipe2.quote_user.add(user2)


    def test_url(self):
        self.client.login(username="sample2", password="pass2")
        user2 = User.objects.get(id=2)
        data = {
            "recipe_name": "recipe_name",
            "ingredient": "ingredient",
            "type": "スープ",
            "user": user2,
            "public": "公開"
            }
        response = self.client.post("/eat/create/quote/1/", data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")

    def test_name(self):
        self.client.login(username="sample2", password="pass2")
        user2 = User.objects.get(id=2)
        data = {
            "recipe_name": "recipe_name",
            "ingredient": "ingredient",
            "type": "スープ",
            "user": user2,
            "public": "公開"
            }
        response = self.client.post(
            reverse("eat:quote_create", kwargs={"pk": 1}),
            data=data,
            follow=True
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")

    def test_name_create_recipe(self):
        print("test2")
        self.client.login(username="sample2", password="pass2")
        user2 = User.objects.get(id=2)
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(str(list(recipe.quote_user.all())), "[]")
        data = {
            "recipe_name": "recipe_name",
            "ingredient": "ingredient",
            "type": "スープ",
            "user": user2,
            "public": "公開"
            }
        response = self.client.post(
            reverse("eat:quote_create", kwargs={"pk": 1}),
            data=data,
            follow=True
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertEqual(str(list(recipe.quote_user.all())), "[<User: sample2>]")
        create_recipe = Recipe.objects.get(id=4)
        self.assertEqual(create_recipe.quote, "有り")
        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]), "参考cookを作成しました")

#すでに参考クックを投稿している場合
    def test_name_created_recipe(self):
        self.client.login(username="sample2", password="pass2")
        user2 = User.objects.get(id=2)
        data = {
            "recipe_name": "recipe_name",
            "ingredient": "ingredient",
            "type": "スープ",
            "user": user2,
            "public": "公開"
            }
        response = self.client.post(
            reverse("eat:quote_create", kwargs={"pk": 2}),
            data=data,
            HTTP_REFERER=str(reverse('signup:top')),
            follow=True
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup/top.html')
        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]), "すでに参考cookを作成しています")

##投稿が参考cookの場合
    def test_name_quote(self):
        self.client.login(username="sample", password="pass")
        data = {
            "recipe_name": "recipe_name",
            "ingredient": "ingredient",
            "type": "スープ",
            "user": self.user,
            "public": "公開"
            }
        response = self.client.post(
            reverse("eat:quote_create", kwargs={"pk": 3}),
            data=data,
            HTTP_REFERER=str(reverse('signup:top')),
            follow=True
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup/top.html')
        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]), "参考cookに参考cookは作成できません")

#投稿者とログインユーザーが一緒の場合
    def test_name_create_my_quote_recipe(self):
        self.client.login(username="sample", password="pass")
        data = {
            "recipe_name": "recipe_name",
            "ingredient": "ingredient",
            "type": "スープ",
            "user": self.user,
            "public": "公開"
            }
        response = self.client.post(
            reverse("eat:quote_create", kwargs={"pk": 1}),
            data=data,
            HTTP_REFERER=str(reverse('signup:top')),
            follow=True
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup/top.html')
        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]), "自分の投稿に参考cookは作成できません")

    def test_not_login(self):
        response = self.client.post(
            reverse("eat:quote_create", kwargs={"pk": 1}),
            follow=True
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

class TestEatUpdateView(TestCase):
    def setUp(self):
        client = Client()
        self.user = User.objects.create_user("sample", "sample@gmail.com", "pass")
        user1_recipe1 = Recipe.objects.create(
            recipe_name="recipe_name1",
            ingredient="ingredient1",
            type="ご飯",
            user=self.user,
            public="公開"
            )

    def test_url(self):
        self.client.login(username="sample", password="pass")
        data = {
            "recipe_name": "recipe_name1",
            "ingredient": "ingredient1",
            "type": "スープ",
            "user": self.user,
            "public": "公開"
            }
        response = self.client.get("/eat/update/1/", data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eat/recipe_update_form.html')


    def test_name_success_messages(self):
        self.client.login(username="sample", password="pass")
        data = {
            "recipe_name": "recipe_name1",
            "ingredient": "ingredient1",
            "type": "スープ",
            "user": self.user,
            "public": "公開"
            }
        response = self.client.post(
            reverse("eat:update", kwargs={'pk':1}),
            data=data,
            follow=True
            )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('eat:detail', kwargs={"pk":1}))
        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]), "投稿を上書きしました")

    def test_name_error_messages(self):
        self.client.login(username="sample", password="pass")
        data = {
            "recipe_name": "recipe_name1",
            "ingredient": "ingredient1",
            "user": self.user,
            "public": "公開"
            }
        response = self.client.post(
            reverse("eat:update", kwargs={'pk':1}),
            data=data,
            follow=True
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_update_form.html")
        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]), "保存に失敗しました")

class TestEatDeleteView(TestCase):
    def setUp(self):
        client = Client()
        self.user = User.objects.create_user("sample", "sample@gmail.com", "pass")
        user1_recipe1 = Recipe.objects.create(
            recipe_name="recipe_name1",
            ingredient="ingredient1",
            type="ご飯",
            user=self.user,
            public="公開"
            )
        user2_recipe2 = Recipe.objects.create(
            recipe_name="recipe_name1",
            ingredient="ingredient1",
            type="ご飯",
            user=self.user,
            public="公開"
            )
        user1_recipe3 = Recipe.objects.create(
            recipe_name="recipe_name1",
            ingredient="ingredient1",
            type="ご飯",
            user=self.user,
            public="公開",
            quote="有り",
            quote_recipe=user2_recipe2,
            )
        user2_recipe2.quote_user.add(self.user)


    def test_url(self):
        self.client.login(username="sample", password="pass")
        response = self.client.post("/eat/delete/1/", follow=True)
        self.assertEqual(response.status_code, 200)
        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]), "消去しました")

    def test_name(self):
        self.client.login(username="sample", password="pass")
        recipe_quote = Recipe.objects.get(id=2)
        self.assertEqual(str(list(recipe_quote.quote_user.all())), "[<User: sample>]")
        response = self.client.post(
            reverse("eat:delete", kwargs={"pk": 3}),
            follow=True
            )
        recipe_quote = Recipe.objects.get(id=2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(list(recipe_quote.quote_user.all())), "[]")
        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]), "消去しました")
