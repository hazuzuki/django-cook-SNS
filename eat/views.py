from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.db.models import Q


from signup.models import User
from eat.models import Recipe
from eat.forms import RecipeForm
from itertools import chain



class OnlyUserRequiredMixin(UserPassesTestMixin):

    raise_exception = True

    def test_func(self):
        user = self.request.user
        obj = get_object_or_404(Recipe, id=self.kwargs['pk'])
        return user.pk == obj.user.id or user.is_superuser

#投稿編集の制限
def good(request, *args, **kwargs):
    if request.user.is_authenticated:
        #いいねする投稿の情報を取得
        recipe = Recipe.objects.get(id=kwargs['pk'])

        #投稿にすでにいいねしている場合
        if Recipe.objects.filter(id=recipe.id, good_user=request.user).exists():
            recipe.good_user.remove(request.user)
            recipe.save()
        else:
            recipe.good_user.add(request.user)
            recipe.save()
    #前回表示していたページにリダイレクト
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect("signup:login")






#いいねのリスト
class EatGoodUsersListView(ListView):
    model = Recipe
    template_name = "eat/recipe_good_users_list.html"
    paginate_by = 20

    def get_queryset(self):
        search = self.request.GET.get("search")
        order = self.request.GET.get("order")
        users_id = self.kwargs.get('users_id')
        users = User.objects.get(id=users_id)

        object_list = Recipe.objects.filter(good_user=users_id)
        #ログイン中
        if self.request.user.is_authenticated:
            #フォローしているユーザーの友達のみ公開の投稿を絞り込む
            object_list = object_list.filter(
                Q(user__in=self.request.user.follow.all(), public="友達のみ")|
                Q(public="公開")
                )
        #ログアウト中
        else:
            object_list = object_list.exclude(
                Q(public="非公開")|
                Q(public="友達のみ")
                )

        if search:
            object_list = object_list.filter(
                Q(good_user=users_id),
                Q(recipe_name__contains=search)|
                Q(ingredient__contains=search)|
                Q(type__contains=search)
                )
            if order == "new":
                object_list = object_list.order_by("-date")
            elif order == "old":
                object_list = object_list.order_by("date")
            else:
                object_list = object_list.order_by("-date")
        elif order == "old":
            object_list = object_list.order_by("date")
        else:
            object_list = object_list.order_by("-date")
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users_id = self.kwargs.get('users_id')
        users = User.objects.get(id=users_id)
        recipe_count = Recipe.objects.filter(user=users).count()
        follower_count = User.objects.filter(follow__username=users).count()
        context["recipe_count"] = recipe_count
        context["users"] = users
        context["follower_count"] = follower_count
        return context


class EatListView(LoginRequiredMixin, ListView):
    model = Recipe
    paginate_by = 20
    login_url = "/signup/login/"

    def get_queryset(self):
        search = self.request.GET.get("search")
        order = self.request.GET.get("order")

        if self.request.user.is_authenticated:
            filter_object = Recipe.objects.filter(user=self.request.user)
            if search:
                filter_object = Recipe.objects.filter(
                    Q(user=self.request.user),
                    Q(recipe_name__contains=search)|
                    Q(ingredient__contains=search)|
                    Q(type__contains=search)
                    )
                if order == "new":
                    object_list = filter_object.order_by("-date")
                elif order == "old":
                    object_list = filter_object
                else:
                    object_list = filter_object.order_by("-date")
            elif order == "old":
                object_list = filter_object
            else:
                object_list = filter_object.order_by("-date")
            return object_list

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            users = User.objects.get(id=self.request.user.id)
            recipe_count = Recipe.objects.filter(user=users).count()
            follower_count = User.objects.filter(follow__username=users).count()
            context["recipe_count"] = recipe_count
            context["users"] = users
            context["follower_count"] = follower_count
            return context

#選択消去
    def post(self, request, **kwargs):
        deletes = request.GET.get("deletes")

        if deletes == "deletes":
            users_id = self.kwargs.get('users_id')
            recipe_pks = request.POST.getlist('delete')
            Recipe.objects.filter(pk__in=recipe_pks).delete()
            return redirect('eat:index')




class EatTimeLineListView(LoginRequiredMixin, ListView):
    model = Recipe
    paginate_by = 20
    login_url = "/signup/login/"
    template_name = "eat/recipe_timeline_list.html"

    def get_queryset(self):
        search = self.request.GET.get("search")
        order = self.request.GET.get("order")

        if self.request.user.is_authenticated:
            filter_object = Recipe.objects.filter(
                Q(user__in=self.request.user.follow.all())|
                Q(user=self.request.user)
                )
            #非公開の投稿は表示しない
            filter_object = filter_object.exclude(public="非公開")
            #検索ワードがある場合
            if search:
                filter_object = filter_object.filter(
                    Q(user__username__contains=search)|
                    Q(recipe_name__contains=search)|
                    Q(ingredient__contains=search)|
                    Q(type__contains=search)
                    )
                #並び替え
                if order == "new":
                    object_list = filter_object.order_by("-date")
                elif order == "old":
                    object_list = filter_object.order_by("date")
                #検索ワードのみの場合
                else:
                    object_list = filter_object.order_by("-date")
            elif order == "old":
                object_list = filter_object.order_by("date")
            else:
                object_list = filter_object.order_by("-date")
            return object_list




class EatUsersListView(ListView):
    model = Recipe
    paginate_by = 5
    login_url = "/signup/login/"
    template_name = "eat/recipe_list.html"

    def get_queryset(self):
        search = self.request.GET.get("search")
        order = self.request.GET.get("order")
        users_id = self.kwargs.get('users_id')
        users = User.objects.get(id=users_id)


        filter_object = Recipe.objects.filter(user=users_id)
        #非公開の投稿を表示させない
        if self.request.user.is_authenticated:
            if users == self.request.user:
                filter_object = filter_object.order_by("-date")
            elif users in self.request.user.follow.all():
                filter_object = filter_object.exclude(public="非公開")
            else:
                filter_object = filter_object.exclude(Q(public="非公開") | Q(public="友達のみ"))
        else:
            filter_object = filter_object.exclude(Q(public="非公開") | Q(public="友達のみ"))
        if search:
            filter_object = filter_object.filter(
                Q(user=users_id),
                Q(recipe_name__contains=search)|
                Q(ingredient__contains=search)|
                Q(type__contains=search))
            if order == "new":
                object_list = filter_object.order_by("-date")
            elif order == "old":
                object_list = filter_object.order_by("date")
            else:
                object_list = filter_object.order_by("-date")
        elif order == "old":
            object_list = filter_object.order_by("date")
        else:
            object_list = filter_object.order_by("-date")
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users_id = self.kwargs.get('users_id')
        users = User.objects.get(id=users_id)
        recipe_count = Recipe.objects.filter(user=users).count()
        follower_count = User.objects.filter(follow__username=users).count()
        context["recipe_count"] = recipe_count
        context["users"] = users
        context["follower_count"] = follower_count
        return context




class EatFindListView(ListView):
    model = Recipe
    paginate_by = 20
    login_url = "/signup/login/"
    template_name = "eat/recipe_find_list.html"

    def get_queryset(self):
        search = self.request.GET.get("search")
        order = self.request.GET.get("order")

        filter_object = Recipe.objects.all()

        #ログインしている場合
        if self.request.user.is_authenticated:
            #ログイン中
            #フォローしているユーザーの友達のみ公開の投稿を絞り込む
            filter_object = filter_object.filter(
                Q(user__in=self.request.user.follow.all(), public="友達のみ")|
                Q(public="公開")|
                Q(user=self.request.user)
                )
        #ログアウト中
        else:
            filter_object = filter_object.exclude(
                Q(public="非公開")|
                Q(public="友達のみ")
                )
        if search:
            filter_object = filter_object.filter(
                Q(recipe_name__contains=search)|
                Q(memo__contains=search)|
                Q(user__username__contains=search)|
                Q(ingredient__contains=search)|
                Q(type__contains=search)
                )
            if order == "new":
                object_list = filter_object.order_by("-date")
            elif order == "old":
                object_list = filter_object.order_by("date")
            else:
                object_list = filter_object.order_by("-date")
        elif order == "old":
            object_list = filter_object.order_by("date")
        else:
            object_list = filter_object.order_by("-date")
        return object_list



class EatDetailView(DetailView):
    model = Recipe
    login_url = "/signup/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe_id = self.kwargs.get("pk")
        object_list = Recipe.objects.filter(quote_recipe=recipe_id)
        context["object_list"] = object_list
        return context

#参考cookの作成
class EatQuoteDetailView(DetailView):
    model = Recipe
    template_name = "eat/quote_recipe.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            recipe = self.get_object()
            #すでに参考クックを投稿している場合
            if Recipe.objects.filter(id=kwargs['pk'], quote_user=self.request.user).exists():
                msg = """このレシピの参考cookは作成済みです。レシピは<a href='{url}'> こちら </a>から削除できます"""
                delete_recipe = Recipe.objects.get(id=kwargs['pk'], quote_user=self.request.user)
                url = reverse_lazy("eat:delete", kwargs={"pk": delete_recipe.id})
                messages.error(self.request, mark_safe(msg.format(url=url)))
                return redirect(request.META.get('HTTP_REFERER'))
            elif recipe.quote == "有り":
                messages.error(self.request, "参考cookに参考cookは作成できません")
                return redirect(request.META.get('HTTP_REFERER'))
            #作成者とログインユーザーが一致しない場合
            elif recipe.user != self.request.user:
                self.object = self.get_object()
                context = self.get_context_data(object=self.object)
                return self.render_to_response(context)
            #投稿者とログインユーザーが一緒の場合
            else:
                return redirect('signup:top')
        else:
            return redirect("signup:login")


class EatCreateView(LoginRequiredMixin, CreateView):
    model = Recipe, User
    form_class = RecipeForm
    template_name = "eat/recipe_create_form.html"
    success_url = reverse_lazy("eat:index")
    login_url = "/signup/login/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "保存しました")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "保存に失敗しました")
        return super().form_invalid(form)

class EatQuoteCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "eat/quote_create.html"
    success_url = reverse_lazy("eat:index")
    login_url = "/signup/login/"

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            recipe = Recipe.objects.get(id=kwargs['pk'])
            #すでに参考クックを投稿している場合
            if Recipe.objects.filter(id=kwargs['pk'], quote_user=self.request.user).exists():
                messages.error(self.request, "すでに参考cookを作成しています")
                return redirect(request.META.get('HTTP_REFERER'))
            #投稿が参考cookの場合
            elif recipe.quote == "有り":
                messages.error(self.request, "参考cookに参考cookは作成できません")
                return redirect(request.META.get('HTTP_REFERER'))
            #作成者とログインユーザーが一致しない場合
            elif recipe.user != self.request.user:
                recipe.quote_user.add(self.request.user)
                recipe.save()
            #投稿者とログインユーザーが一緒の場合
            else:
                messages.error(self.request, "自分の投稿に参考cookは作成できません")
                return redirect(request.META.get('HTTP_REFERER'))


        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        #qupte_recipeを追加する
        form.instance.quote_recipe = Recipe.objects.get(id=self.kwargs.get('pk'))
        form.instance.quote = "有り"
        messages.success(self.request, "参考cookを作成しました")
        return super().form_valid(form)

class EatUpdateView(LoginRequiredMixin, OnlyUserRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "eat/recipe_update_form.html"
    login_url = "/signup/login/"

    def get_success_url(self):
        url = reverse_lazy("eat:detail", kwargs={"pk":self.kwargs["pk"]})
        return url

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "投稿を上書きしました")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "保存に失敗しました")
        return super().form_invalid(form)


class EatDeleteView(LoginRequiredMixin, OnlyUserRequiredMixin, DeleteView):
    model = Recipe
    template_name = "eat/recipe_delete.html"
    success_url = reverse_lazy("eat:index")
    login_url = "/signup/login/"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.quote == "有り":
            if self.object.quote_recipe:
                recipe_quoted = Recipe.objects.get(id=self.object.quote_recipe.id)
                recipe_quoted.quote_user.remove(request.user)
                recipe_quoted.save()
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "消去しました")
        return super().delete(request, *args, **kwargs)
