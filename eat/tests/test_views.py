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



class Good(TestCase):
    def setUp(self):
        client = Client()
        self.user = User.objects.create_user("sample", "sample@gmail.com", "pass")

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
        response = self.client.get(reverse('eat:good', kwargs={'pk': 1}), HTTP_REFERER=str(reverse('eat:find')) , follow=True)
        self.assertEqual(response.status_code, 200)
        recipe = Recipe.objects.get(id=1)
        users = User.objects.filter(username='sample')
        self.assertEqual(list(recipe.good_user.all()), list(users))

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
        self.assertEqual(str(recipe.good_user.all()), "<QuerySet []>")
        response = self.client.get('/eat/1/', HTTP_REFERER=str(reverse('eat:find')) , follow=True)
        self.assertEqual(response.status_code, 200)
        recipe = Recipe.objects.get(id=1)
        users = User.objects.filter(username='sample')
        self.assertEqual(list(recipe.good_user.all()), list(users))

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
        response = self.client.get(reverse('eat:good', kwargs={'pk': 1}), HTTP_REFERER=str(reverse('eat:find')) , follow=True)
        self.assertEqual(response.status_code, 200)
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(str(recipe.good_user.all()), "<QuerySet []>")

    def test_recipe_object_good_url(self):
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
        response = self.client.get('/eat/1/', HTTP_REFERER=str(reverse('eat:find')) , follow=True)
        self.assertEqual(response.status_code, 200)
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(str(recipe.good_user.all()), "<QuerySet []>")

    def test_good_not_login(self):
        response = self.client.get('/eat/1/', HTTP_REFERER=str(reverse('eat:find')) , follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")


class EatGoodUserListView(TestCase):
    def setUp(self):
        client = Client()
        self.user = User.objects.create_user("sample", "sample@gmail.com", "pass")
        user2 = User.objects.create_user("sample2", "sample2@gmail.com", "pass2")
        user3 = User.objects.create_user("sample3", "sample3@gmail.com", "pass3")
        #self.userのオブジェクト
        user_recipe1 = Recipe.objects.create(
            recipe_name="sample_recipe_name1",
            site="sample.url1",
            memo="sample_memo1",
            photo="sample.img1",
            ingredient="sample_ingredient1",
            type="ご飯",
            date="2018-10-25 14:30:59",
            user=self.user,
            public="公開"
            )
        user_recipe2 = Recipe.objects.create(
            recipe_name="sample_recipe_name1",
            site="sample.url1",
            memo="sample_memo1",
            photo="sample.img1",
            ingredient="sample_ingredient1",
            type="ご飯",
            date="2018-10-25 14:30:59",
            user=self.user,
            public="非公開"
            )
        recipe2 = Recipe.objects.create(
            recipe_name="sample_recipe_name2",
            site="sample.url2",
            memo="sample_memo2",
            photo="sample.img2",
            ingredient="sample_ingredient2",
            type="ご飯",
            date="2018-10-25 14:30:59",
            user=user2,
            public="公開"
            )
        recipe3 = Recipe.objects.create(
            recipe_name="sample_recipe_name3",
            site="sample.url3",
            memo="sample_memo3",
            photo="sample.img3",
            ingredient="sample_ingredient3",
            type="ご飯",
            date="2018-10-25 14:30:59",
            user=user2,
            public="非公開"
            )
        recipe4 = Recipe.objects.create(
            recipe_name="sample_recipe_name3",
            site="sample.url3",
            memo="sample_memo3",
            photo="sample.img3",
            ingredient="sample_ingredient3",
            type="ご飯",
            date="2018-10-25 14:30:59",
            user=users,
            )

    def test_url_none_object(self):

        self.client.login(username="sample", password="pass")
        response = self.client.get("/eat/list/1/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_good_users_list.html")
        print(response.context["recipe_count"])




#delateView アクセスのしかた
#object作成
#検索、並び替えのテスト未
#投稿が１つと２つで場合わけ
class TestEatListView(TestCase):
#ユーザー作成　ログイン
    def setUp(self):
        client = Client()
        self.user = User.objects.create_user("sample", "sample@gmail.com", "pass")

#投稿なし　url
    def test_url_none_object(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get("/eat/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")

#投稿なし　name
    def test_name_none_object(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(reverse("eat:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertQuerysetEqual(response.context["recipe_list"], [])
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == False)
        self.assertEqual(len(response.context['recipe_list']), 0)

#投稿１つ　url
    def test_url_one_object(self):
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
        response = self.client.get("/eat/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")


#投稿１つ　name
    def test_name_one_object(self):
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
        object_list = Recipe.objects.filter(user=self.user).order_by("-date")
        response = self.client.get(reverse("eat:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertEqual(str(response.context["user"]), "sample")
        self.assertQuerysetEqual(list(response.context["recipe_list"]), [repr(s) for s in object_list])
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == False)
        self.assertEqual(len(response.context['recipe_list']), 1)
        self.assertContains(response, "sample_recipe_name")
        self.assertContains(response, "sample.img")
        self.assertContains(response, "sample_ingredient")
        self.assertContains(response, "ご飯")



#投稿２つ　name
    def test_two_objeccts(self):
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
        recipe2 = Recipe.objects.create(
            recipe_name="sample_recipe_name2",
            site="sample.url2",
            memo="sample_memo2",
            photo="sample.img2",
            ingredient="sample_ingredient2",
            type="ご飯",
            date="2018-10-25 14:30:59",
            user=self.user,
            )
        object_list = Recipe.objects.filter(user=self.user).order_by("-date")
        response = self.client.get(reverse("eat:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertEqual(str(response.context["user"]), "sample")
        self.assertQuerysetEqual(list(response.context["recipe_list"]), [repr(s) for s in object_list])
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == False)
        self.assertEqual(len(response.context["recipe_list"]), 2)
        self.assertContains(response, "sample_recipe_name")
        self.assertContains(response, "sample.img")
        self.assertContains(response, "sample_ingredient")
        self.assertContains(response, "ご飯")
        self.assertContains(response, "sample_recipe_name2")
        self.assertContains(response, "sample.img2")
        self.assertContains(response, "sample_ingredient2")
        self.assertContains(response, "ご飯")




#1ページ目　url
    def test_url_pagination_pagi1(self):
        self.client.login(username="sample", password="pass")
        number_of_recipe = 8
        for recipe in range(number_of_recipe):
            Recipe.objects.create(
                recipe_name="sample",
                site="sample.url",
                memo="sample",
                photo="sample.img",
                ingredient="sample",
                type="ご飯",
                date="2018-10-25 14:30:59",
                user=self.user,
                )
        self.client.login(username="sample", password="pass")
        response = self.client.get("/eat/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")


#1ページ目　name
    def test_name_pagination_pagi1(self):
        self.client.login(username="sample", password="pass")
        number_of_recipe = 8
        for recipe in range(number_of_recipe):
            Recipe.objects.create(
                recipe_name="sample",
                site="sample.url",
                memo="sample",
                photo="sample.img",
                ingredient="sample",
                type="ご飯",
                date="2018-10-25 14:30:59",
                user=self.user,
                )
        object_list = Recipe.objects.filter(user=self.user).order_by("-date")
        object_list = object_list[:5]
        self.client.login(username="sample", password="pass")
        response = self.client.get(reverse("eat:index") + "?page=1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertEqual(str(response.context["user"]), "sample")
        self.assertQuerysetEqual(list(response.context["recipe_list"]), [repr(s) for s in object_list])
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["recipe_list"]), 5)

#2ページ目　name
    def test_name_pagination_pagi2(self):
        self.client.login(username="sample", password="pass")
        number_of_recipe = 8
        for recipe in range(number_of_recipe):
            Recipe.objects.create(
                recipe_name="sample",
                site="sample.url",
                memo="sample",
                photo="sample.img",
                ingredient="sample",
                type="ご飯",
                date="2018-10-25 14:30:59",
                user=self.user,
                )
        object_list = Recipe.objects.filter(user=self.user).order_by("-date")
        object_list = object_list[5:10]
        self.client.login(username="sample", password="pass")
        response = self.client.get(reverse("eat:index") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertEqual(str(response.context["user"]), "sample")
        self.assertQuerysetEqual(list(response.context["recipe_list"]), [repr(s) for s in object_list])
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["recipe_list"]), 3)

#ログインしていない時　url
    def test_url_not_login(self):
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
        response = self.client.get("/eat/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/signup/login/?next=/eat/')



#ログインしていない時　name
    def test_name_not_login(self):
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
        response = self.client.get(reverse("eat:index"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/signup/login/?next=/eat/')


#並び替え
    def test_name_order_new(self):
        self.client.login(username="sample", password="pass")
        recipe1 = Recipe.objects.create(
            recipe_name="sample1",
            site="sample.url1",
            memo="sample_memo1",
            photo="sample.img1",
            ingredient="sample_ingredient1",
            type="ご飯",
            )
        recipe2 = Recipe.objects.create(
            recipe_name="sample2",
            site="sample.url2",
            memo="sample_memo2",
            photo="sample.img2",
            ingredient="sample_ingredient1",
            type="ご飯",
            )
        recipe3 = Recipe.objects.create(
            recipe_name="sample3",
            site="sample.url3",
            memo="sample_memo3",
            photo="sample.img3",
            ingredient="sample_ingredient3",
            type="ご飯",
            )
        object_list = Recipe.objects.filter(user=self.user).order_by("-date")
        response = self.client.get(reverse("eat:index"), {'order':'new'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertQuerysetEqual(list(response.context["recipe_list"]), [repr(s) for s in object_list])

    def test_name_order_old(self):
        self.client.login(username="sample", password="pass")
        recipe1 = Recipe.objects.create(
            recipe_name="sample1",
            site="sample.url1",
            memo="sample_memo1",
            photo="sample.img1",
            ingredient="sample_ingredient1",
            type="ご飯",
            )
        recipe2 = Recipe.objects.create(
            recipe_name="sample2",
            site="sample.url2",
            memo="sample_memo2",
            photo="sample.img2",
            ingredient="sample_ingredient1",
            type="ご飯",
            )
        recipe3 = Recipe.objects.create(
            recipe_name="sample3",
            site="sample.url3",
            memo="sample_memo3",
            photo="sample.img3",
            ingredient="sample_ingredient3",
            type="ご飯",
            )
        object_list = Recipe.objects.filter(user=self.user)
        response = self.client.get(reverse("eat:index"), {'order':'old'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertQuerysetEqual(list(response.context["recipe_list"]), [repr(s) for s in object_list])


    def test_name_filter(self):
        self.client.login(username="sample", password="pass")
        recipe1 = Recipe.objects.create(
            recipe_name="sample1",
            site="sample.url1",
            memo="sample_memo1",
            photo="sample.img1",
            ingredient="sample_ingredient1",
            type="ご飯",
            )
        recipe2 = Recipe.objects.create(
            recipe_name="sample2",
            site="sample.url2",
            memo="sample_memo2",
            photo="sample.img2",
            ingredient="sample_ingredient1",
            type="ご飯",
            )
        recipe3 = Recipe.objects.create(
            recipe_name="sample3",
            site="sample.url3",
            memo="sample_memo3",
            photo="sample.img3",
            ingredient="sample_ingredient3",
            type="ご飯",
            )
        search = "肉じゃが"
        object_list = Recipe.objects.filter(
            Q(user=self.user),
            Q(recipe_name__contains=search)|
            Q(ingredient__contains=search)|
            Q(type__contains=search)
            ).order_by("-date")
        response = self.client.get(reverse("eat:index"), {'search':'肉じゃが'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertQuerysetEqual(list(response.context["recipe_list"]), [repr(s) for s in object_list])


    def test_name_order_filter_none_object(self):
        self.client.login(username="sample", password="pass")
        recipe1 = Recipe.objects.create(
            recipe_name="sample1",
            site="sample.url1",
            memo="sample_memo1",
            photo="sample.img1",
            ingredient="sample_ingredient1",
            type="ご飯",
            )
        recipe2 = Recipe.objects.create(
            recipe_name="sample2",
            site="sample.url2",
            memo="sample_memo2",
            photo="sample.img2",
            ingredient="sample_ingredient1",
            type="ご飯",
            )
        recipe3 = Recipe.objects.create(
            recipe_name="sample3",
            site="sample.url3",
            memo="sample_memo3",
            photo="sample.img3",
            ingredient="sample_ingredient3",
            type="ご飯",
            )
        search = "カーテン"
        object_list = Recipe.objects.filter(
            Q(user=self.user),
            Q(recipe_name__contains=search)|
            Q(ingredient__contains=search)|
            Q(type__contains=search)
            ).order_by("-date")
        response = self.client.get(reverse("eat:index"), {'search':'カーテン'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertQuerysetEqual(list(response.context["recipe_list"]), [repr(s) for s in object_list])

    def test_name_order_filter_none(self):
        self.client.login(username="sample", password="pass")
        recipe1 = Recipe.objects.create(
            recipe_name="sample1",
            site="sample.url1",
            memo="sample_memo1",
            photo="sample.img1",
            ingredient="sample_ingredient1",
            type="ご飯",
            )
        recipe2 = Recipe.objects.create(
            recipe_name="sample2",
            site="sample.url2",
            memo="sample_memo2",
            photo="sample.img2",
            ingredient="sample_ingredient1",
            type="ご飯",
            )
        recipe3 = Recipe.objects.create(
            recipe_name="sample3",
            site="sample.url3",
            memo="sample_memo3",
            photo="sample.img3",
            ingredient="sample_ingredient3",
            type="ご飯",
            )
        search = ""
        object_list = Recipe.objects.filter(
            Q(user=self.user),
            Q(recipe_name__contains=search)|
            Q(ingredient__contains=search)|
            Q(type__contains=search)
            ).order_by("-date")
        response = self.client.get(reverse("eat:index"), {'search':''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertQuerysetEqual(list(response.context["recipe_list"]), [repr(s) for s in object_list])

    def test_name_order_new_filter(self):
        self.client.login(username="sample", password="pass")
        self.client.login(username="sample", password="pass")
        recipe1 = Recipe.objects.create(
            recipe_name="sample1",
            site="sample.url1",
            memo="sample_memo1",
            photo="sample.img1",
            ingredient="sample_ingredient1",
            type="ご飯",
            )
        recipe2 = Recipe.objects.create(
            recipe_name="sample2",
            site="sample.url2",
            memo="sample_memo2",
            photo="sample.img2",
            ingredient="sample_ingredient1",
            type="ご飯",
            )
        recipe3 = Recipe.objects.create(
            recipe_name="sample3",
            site="sample.url3",
            memo="sample_memo3",
            photo="sample.img3",
            ingredient="sample_ingredient3",
            type="ご飯",
            )
        search = "にんじん"
        object_list = Recipe.objects.filter(
            Q(user=self.user),
            Q(recipe_name__contains=search)|
            Q(ingredient__contains=search)|
            Q(type__contains=search)
            ).order_by("-date")
        response = self.client.get(reverse("eat:index"), {'order':'new', 'search':'にんじん'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertQuerysetEqual(list(response.context["recipe_list"]), [repr(s) for s in object_list])

    def test_name_order_old_filter(self):
        self.client.login(username="sample", password="pass")
        recipe1 = Recipe.objects.create(
            recipe_name="sample1",
            site="sample.url1",
            memo="sample_memo1",
            photo="sample.img1",
            ingredient="sample_ingredient1",
            type="ご飯",
            )
        recipe2 = Recipe.objects.create(
            recipe_name="sample2",
            site="sample.url2",
            memo="sample_memo2",
            photo="sample.img2",
            ingredient="sample_ingredient1",
            type="ご飯",
            )
        recipe3 = Recipe.objects.create(
            recipe_name="sample3",
            site="sample.url3",
            memo="sample_memo3",
            photo="sample.img3",
            ingredient="sample_ingredient3",
            type="ご飯",
            )
        search = "にんじん"
        object_list = Recipe.objects.filter(
            Q(user=self.user),
            Q(recipe_name__contains=search)|
            Q(ingredient__contains=search)|
            Q(type__contains=search)
            ).order_by("-date")
        response = self.client.get(reverse("eat:index"), {'order':'old', 'search':'にんじん'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertQuerysetEqual(list(response.context["recipe_list"]), [repr(s) for s in object_list])

    def test_name_pagination_pagi1_serch_order_new(self):
        self.client.login(username="sample", password="pass")
        number_of_recipe = 8
        for recipe in range(number_of_recipe):
            recipe = recipe+1
            Recipe.objects.create(
                recipe_name="sample"+str(recipe),
                site="sample.url",
                memo="sample",
                photo="sample.img",
                ingredient="にんじん",
                type="ご飯",
                )
        recipe9 = Recipe.objects.create(
            recipe_name="sample9",
            site="sample.url",
            memo="sample",
            photo="sample.img",
            ingredient="じゃがいも",
            type="ご飯",
            )
        search = "にんじん"
        object_list = Recipe.objects.filter(
            Q(user=self.user),
            Q(recipe_name__contains=search)|
            Q(ingredient__contains=search)|
            Q(type__contains=search)
            ).order_by("-date")
        object_list = object_list[:5]
        response = self.client.get("/eat/?page=1&search=にんじん&order=new")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertQuerysetEqual(list(response.context["recipe_list"]), [repr(s) for s in object_list])
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["recipe_list"]), 5)

    def test_name_pagination_pagi2_serch_order_new(self):
        self.client.login(username="sample", password="pass")
        number_of_recipe = 8
        for recipe in range(number_of_recipe):
            recipe = recipe+1
            Recipe.objects.create(
                recipe_name="sample"+str(recipe),
                site="sample.url",
                memo="sample",
                photo="sample.img",
                ingredient="にんじん",
                type="ご飯",
                )
        recipe9 = Recipe.objects.create(
            recipe_name="sample9",
            site="sample.url",
            memo="sample",
            photo="sample.img",
            ingredient="じゃがいも",
            type="ご飯",
            )
        search = "にんじん"
        object_list = Recipe.objects.filter(
            Q(user=self.user),
            Q(recipe_name__contains=search)|
            Q(ingredient__contains=search)|
            Q(type__contains=search)
            ).order_by("-date")
        object_list = object_list[5:10]
        response = self.client.get("/eat/?page=2&search=にんじん&order=new")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertQuerysetEqual(list(response.context["recipe_list"]), [repr(s) for s in object_list])
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["recipe_list"]), 3)

    def test_name_pagination_pagi1_serch_order_old(self):
        self.client.login(username="sample", password="pass")
        number_of_recipe = 8
        for recipe in range(number_of_recipe):
            recipe = recipe+1
            Recipe.objects.create(
                recipe_name="sample"+str(recipe),
                site="sample.url",
                memo="sample",
                photo="sample.img",
                ingredient="にんじん",
                type="ご飯",
                )
        recipe9 = Recipe.objects.create(
            recipe_name="sample9",
            site="sample.url",
            memo="sample",
            photo="sample.img",
            ingredient="じゃがいも",
            type="ご飯",
            )
        search = "にんじん"
        object_list = Recipe.objects.filter(
            Q(user=self.user),
            Q(recipe_name__contains=search)|
            Q(ingredient__contains=search)|
            Q(type__contains=search)
            ).order_by("-date")
        object_list = object_list[:5]
        response = self.client.get("/eat/?page=1&search=にんじん&order=old")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertQuerysetEqual(list(response.context["recipe_list"]), [repr(s) for s in object_list])
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["recipe_list"]), 5)

    def test_name_pagination_pagi2_serch_order_old(self):
        self.client.login(username="sample", password="pass")
        number_of_recipe = 8
        for recipe in range(number_of_recipe):
            recipe = recipe+1
            Recipe.objects.create(
                recipe_name="sample"+str(recipe),
                site="sample.url",
                memo="sample",
                photo="sample.img",
                ingredient="にんじん",
                type="ご飯",
                )
        recipe9 = Recipe.objects.create(
            recipe_name="sample9",
            site="sample.url",
            memo="sample",
            photo="sample.img",
            ingredient="じゃがいも",
            type="ご飯",
            )
        search = "にんじん"
        object_list = Recipe.objects.filter(
            Q(user=self.user),
            Q(recipe_name__contains=search)|
            Q(ingredient__contains=search)|
            Q(type__contains=search)
            ).order_by("-date")
        object_list = object_list[5:10]
        response = self.client.get("/eat/?page=2&search=にんじん&order=old")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertQuerysetEqual(list(response.context["recipe_list"]), [repr(s) for s in object_list])
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["recipe_list"]), 3)

    def test_name_pagination_pagi1_order_old(self):
        self.client.login(username="sample", password="pass")
        number_of_recipe = 8
        for recipe in range(number_of_recipe):
            recipe = recipe+1
            Recipe.objects.create(
                recipe_name="sample"+str(recipe),
                site="sample.url",
                memo="sample",
                photo="sample.img",
                ingredient="にんじん",
                type="ご飯",
                )
        recipe9 = Recipe.objects.create(
            recipe_name="sample9",
            site="sample.url",
            memo="sample",
            photo="sample.img",
            ingredient="じゃがいも",
            type="ご飯",
            )
        object_list = Recipe.objects.filter(user=self.user)
        object_list = object_list[:5]
        response = self.client.get("/eat/?page=1&order=old")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertQuerysetEqual(list(response.context["recipe_list"]), [repr(s) for s in object_list])
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["recipe_list"]), 5)

    def test_name_pagination_pagi2_order_old(self):
        self.client.login(username="sample", password="pass")
        number_of_recipe = 8
        for recipe in range(number_of_recipe):
            recipe = recipe+1
            Recipe.objects.create(
                recipe_name="sample"+str(recipe),
                site="sample.url",
                memo="sample",
                photo="sample.img",
                ingredient="にんじん",
                type="ご飯",
                )
        recipe9 = Recipe.objects.create(
            recipe_name="sample9",
            site="sample.url",
            memo="sample",
            photo="sample.img",
            ingredient="じゃがいも",
            type="ご飯",
            )
        object_list = Recipe.objects.filter(user=self.user)
        object_list = object_list[5:10]
        response = self.client.get("/eat/?page=2&order=old")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertQuerysetEqual(list(response.context["recipe_list"]), [repr(s) for s in object_list])
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["recipe_list"]), 4)

    def test_name_pagination_pagi1_serch(self):
        self.client.login(username="sample", password="pass")
        number_of_recipe = 8
        for recipe in range(number_of_recipe):
            recipe = recipe+1
            Recipe.objects.create(
                recipe_name="sample"+str(recipe),
                site="sample.url",
                memo="sample",
                photo="sample.img",
                ingredient="にんじん",
                type="ご飯",
                )
        recipe9 = Recipe.objects.create(
            recipe_name="sample9",
            site="sample.url",
            memo="sample",
            photo="sample.img",
            ingredient="じゃがいも",
            type="ご飯",
            )
        search = "にんじん"
        object_list = Recipe.objects.filter(
            Q(user=self.user),
            Q(recipe_name__contains=search)|
            Q(ingredient__contains=search)|
            Q(type__contains=search)
            ).order_by("-date")
        object_list = object_list[:5]
        response = self.client.get("/eat/?page=1&search=にんじん")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertQuerysetEqual(list(response.context["recipe_list"]), [repr(s) for s in object_list])
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["recipe_list"]), 5)

    def test_name_pagination_pagi2_serch(self):
        self.client.login(username="sample", password="pass")
        number_of_recipe = 8
        for recipe in range(number_of_recipe):
            recipe = recipe+1
            Recipe.objects.create(
                recipe_name="sample"+str(recipe),
                site="sample.url",
                memo="sample",
                photo="sample.img",
                ingredient="にんじん",
                type="ご飯",
                )
        recipe9 = Recipe.objects.create(
            recipe_name="sample9",
            site="sample.url",
            memo="sample",
            photo="sample.img",
            ingredient="じゃがいも",
            type="ご飯",
            )
        search = "にんじん"
        object_list = Recipe.objects.filter(
            Q(user=self.user),
            Q(recipe_name__contains=search)|
            Q(ingredient__contains=search)|
            Q(type__contains=search)
            ).order_by("-date")
        object_list = object_list[5:10]
        response = self.client.get("/eat/?page=2&search=にんじん")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertQuerysetEqual(list(response.context["recipe_list"]), [repr(s) for s in object_list])
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["recipe_list"]), 3)

    def test_name_delete(self):
        self.client.login(username="sample", password="pass")
        recipe1 = Recipe.objects.create(
            recipe_name="ロールキャベツ",
            site="sample.url1",
            memo="sample_memo1",
            photo="sample.img1",
            ingredient="sample_ingredient1",
            type="ご飯",
            )
        recipe2 = Recipe.objects.create(
            recipe_name="肉じゃが",
            site="sample.url2",
            memo="sample_memo2",
            photo="sample.img2",
            ingredient="にんじん",
            type="ご飯",
            )
        recipe3 = Recipe.objects.create(
            recipe_name="トマトスープ",
            site="sample.url3",
            memo="sample_memo3",
            photo="sample.img3",
            ingredient="にんじん",
            type="ご飯",
            )
        object_list = Recipe.objects.filter(user=self.user).order_by("-date")
        response = self.client.get(reverse("eat:index"), {'deletes':'deletes'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertQuerysetEqual(list(response.context["recipe_list"]), [repr(s) for s in object_list])
        recipe_pks = ['1']
        Recipe.objects.filter(pk__in=recipe_pks).delete()
        object_list = Recipe.objects.filter(user=self.user).order_by("-date")
        response = self.client.get(reverse("eat:index"))
        self.assertTemplateUsed(response, "eat/recipe_list.html")
        self.assertQuerysetEqual(list(response.context["recipe_list"]), [repr(s) for s in object_list])


class TestEatDetailView(TestCase):
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
            )

    def test_url_none_object(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get("/eat/detail/2/")
        self.assertEqual(response.status_code, 404)

    def test_name_none_object(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(reverse("eat:detail", kwargs={'pk':2}))
        self.assertEqual(response.status_code, 404)

    def test_url(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get("/eat/detail/1/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_detail.html")

    def test_name(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(reverse("eat:detail", kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_detail.html")
        self.assertEqual(str(response.context["user"]), "sample")
        self.assertContains(response, "sample_recipe_name")
        self.assertContains(response, "sample.url")
        self.assertContains(response, "sample_memo")
        self.assertContains(response, "sample.img")
        self.assertContains(response, "sample_ingredient")
        self.assertContains(response, "ご飯")
        self.assertContains(response, self.user)

    def test_url_not_login(self):
        response = self.client.get("/eat/detail/1/")
        self.assertEqual(response.status_code, 403)

    def test_name_not_login(self):
        response = self.client.get(reverse("eat:detail", kwargs={'pk':1}))
        self.assertEqual(response.status_code, 403)



class TestEatCreateView(TestCase):
    def setUp(self):
        client = Client()
        self.user = User.objects.create_user("sample", "sample@gmail.com", "pass")

    def test_url_post_data(self):
        self.client.login(username="sample", password="pass")
        data = {
            "recipe_name": "sample_recipe_name",
            "site": "sample.url",
            "memo": "sample_memo",
            "photo": 'img/smIMGL3647_TP_V.jpg',
            "ingredient": "sample_ingredient",
            "type": "スープ",
            }
        response = self.client.post("/eat/create/", data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('eat:index'))


    def test_name_post_data(self):
        self.client.login(username="sample", password="pass")
        data = {
            "recipe_name": "sample_recipe_name",
            "site": "sample.url",
            "memo": "sample_memo",
            "photo": 'sample.img',
            "ingredient": "sample_ingredient",
            "type": "スープ",
            }
        response = self.client.post(reverse('eat:create'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('eat:index'))

    def test_name_success_messages(self):
        self.client.login(username="sample", password="pass")
        data = {
            "recipe_name": "sample_recipe_name",
            "site": "sample.url",
            "memo": "sample_memo",
            "photo": 'sample.img',
            "ingredient": "sample_ingredient",
            "type": "スープ",
            }
        response = self.client.post(reverse('eat:create'), data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('eat:index'))
        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]), "保存しました")

    def test_name_get_data(self):
        self.client.login(username="sample", password="pass")
        data = {
            "recipe_name": "sample_recipe_name",
            "site": "sample.url",
            "memo": "sample_memo",
            "photo": 'sample.img',
            "ingredient": "sample_ingredient",
            "type": "スープ",
            }
        response = self.client.get(reverse('eat:create'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_create_form.html")

    def test_name_post_none_data(self):
        self.client.login(username="sample", password="pass")
        data = {}
        response = self.client.post(reverse('eat:create'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_create_form.html")
        self.assertFormError(response, 'form', 'recipe_name', 'このフィールドは必須です。')
        self.assertFormError(response, 'form', 'ingredient', 'このフィールドは必須です。')
        self.assertFormError(response, 'form', 'type', 'このフィールドは必須です。')

    def test_name_error_messages(self):
        self.client.login(username="sample", password="pass")
        data = {}
        response = self.client.post(reverse('eat:create'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_create_form.html")
        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]), "保存に失敗しました")


    def test_name_post_required(self):
        self.client.login(username="sample", password="pass")
        data = {
            "recipe_name": "sample_recipe_name",
            "memo": "sample_memo",
            "ingredient": "sample_ingredient",
            "type": "スープ",
            }
        response = self.client.post(reverse('eat:create'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('eat:index'))


    def test_name_post_none_required(self):
        self.client.login(username="sample", password="pass")
        data = {
            "ingredient": "sample_ingredient",
            "type": "スープ",
            }
        response = self.client.post(reverse('eat:create'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_create_form.html")
        self.assertContains(response, 'errorlist')
        self.assertFormError(response, 'form', 'recipe_name', 'このフィールドは必須です。')
        self.assertEqual(str(response.context['user']), 'sample')
        #投稿できなかった時の初期値のテスト　Bound=False でcontextは使えない？
        self.assertContains(response, "sample_ingredient")
        self.assertContains(response, "スープ")


    def test_url_not_login(self):
        response = self.client.post("/eat/create/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/signup/login/?next=/eat/create/')


    def test_url_not_login(self):
        response = self.client.post(reverse("eat:create"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/signup/login/?next=/eat/create/')



class TestEatUpdateView(TestCase):
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
            )

    def test_url_none_object(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get("/eat/update/2/")
        self.assertEqual(response.status_code, 404)

    def test_name_none_object(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(reverse('eat:update', kwargs={'pk': 2}),)
        self.assertEqual(response.status_code, 404)

    def test_url(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get("/eat/update/1/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_update_form.html")

    def test_name(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(reverse("eat:update", kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_update_form.html")
        self.assertEqual(str(response.context["user"]), "sample")
        self.assertEqual(response.context['form'].initial['recipe_name'], 'sample_recipe_name')
        self.assertEqual(response.context['form'].initial['site'], 'sample.url')
        self.assertEqual(response.context['form'].initial['memo'], 'sample_memo')
        self.assertEqual(response.context['form'].initial['photo'], 'sample.img')
        self.assertEqual(response.context['form'].initial['ingredient'], 'sample_ingredient')
        self.assertEqual(response.context['form'].initial['type'], 'ご飯')


    def test_name_update_post(self):
        self.client.login(username="sample", password="pass")
        data = {
            "recipe_name": "sample_recipe_name",
            "site": "sample.url",
            "memo": "sample_memo",
            "photo": 'sample.img',
            "ingredient": "sample_ingredient",
            "type": "スープ",
            }
        response = self.client.post(reverse("eat:update", kwargs={'pk':1}), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('eat:detail', kwargs={"pk":1}))

    def test_name_success_messages(self):
        self.client.login(username="sample", password="pass")
        data = {
            "recipe_name": "sample_recipe_name",
            "site": "sample.url",
            "memo": "sample_memo",
            "photo": 'sample.img',
            "ingredient": "sample_ingredient",
            "type": "スープ",
            }
        response = self.client.post(reverse("eat:update", kwargs={'pk':1}), data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('eat:detail', kwargs={"pk":1}))
        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]), "投稿を上書きしました")

    def test_name_update_get(self):
        self.client.login(username="sample", password="pass")
        data = {
            "recipe_name": "sample_recipe_name",
            "site": "sample.url",
            "memo": "sample_memo",
            "photo": 'sample.img',
            "ingredient": "sample_ingredient",
            "type": "スープ",
            }
        response = self.client.get(reverse("eat:update", kwargs={'pk':1}), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_update_form.html")

    def test_name_update_post_none_required(self):
        self.client.login(username="sample", password="pass")
        data = {
            "ingredient": "sample_ingredient",
            "type": "スープ",
            }
        response = self.client.post(reverse("eat:update", kwargs={'pk':1}), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_update_form.html")
        self.assertContains(response, 'errorlist')
        self.assertFormError(response, 'form', 'recipe_name', 'このフィールドは必須です。')
        self.assertEqual(str(response.context['user']), 'sample')
        self.assertContains(response, "sample_ingredient")
        self.assertContains(response, "スープ")

    def test_name_error_messages(self):
        self.client.login(username="sample", password="pass")
        data = {
            "ingredient": "sample_ingredient",
            "type": "スープ",
            }
        response = self.client.post(reverse("eat:update", kwargs={'pk':1}), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_update_form.html")
        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]), "保存に失敗しました")


    def test_url_not_login(self):
        response = self.client.get("/eat/update/1/")
        self.assertEqual(response.status_code, 403)

    def test_name_not_login(self):
        response = self.client.get(reverse("eat:update", kwargs={'pk':1}))
        self.assertEqual(response.status_code, 403)



class TestEatDeleteView(TestCase):
    def setUp(self):
        client = Client()
        self.user = User.objects.create_user("sample", "sample@gmail.com", "pass")
        recipe = Recipe.objects.create(
            recipe_name="sample_recipe_name",
            site="sample.url",
            memo="sample_memo",
            photo="sample.img",
            ingredient="sample_ingredient",
            type="ご飯",)

    def test_url_none_object(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get("/eat/delete/2/")
        self.assertEqual(response.status_code, 404)

    def test_name_none_object(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(reverse('eat:delete', kwargs={'pk': 2}),)
        self.assertEqual(response.status_code, 404)

    def test_url_get(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get("/eat/delete/1/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_delete.html")

    def test_name_get(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(reverse("eat:delete", kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_delete.html")
        self.assertEqual(str(response.context["user"]), "sample")

    def test_name_post_delete(self):
        self.client.login(username="sample", password="pass")
        response = self.client.post(reverse("eat:delete", kwargs={'pk':1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("eat:index"))
        response = self.client.get(reverse('eat:delete', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 404)

    def test_name_success_messages(self):
        self.client.login(username="sample", password="pass")
        response = self.client.post(reverse("eat:delete", kwargs={'pk':1}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("eat:index"))
        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]), "消去しました")


    def test_url_not_login(self):
        response = self.client.get("/eat/delete/1/")
        self.assertEqual(response.status_code, 403)

    def test_name_not_login(self):
        response = self.client.get(reverse("eat:delete", kwargs={'pk':1}))
        self.assertEqual(response.status_code, 403)
