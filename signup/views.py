from django.shortcuts import render, redirect

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib import messages


from django.views.generic import FormView, TemplateView, UpdateView, ListView
#from django.views.generic.base import View
from django.views import View

from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from signup.models import User
from signup.forms import CustomUserCreationForm, CustomUserChangeForm, CustomUpdateForm
from eat.models import Recipe


# Create your views here.


class LogoutRequiredMixin(View):
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("eat:index")
        return super().dispatch(*args, **kwargs)

class OnlyMixin(UserPassesTestMixin):

    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser



def follow(request, *args, **kwargs):
    #閲覧中のユーザー取得
    look_user = User.objects.get(id=kwargs['pk'])

    if request.user.is_authenticated:
        #自分はフォローできないようにする
        if look_user != request.user:
            #閲覧中のユーザーをフォローしている場合
            if User.objects.filter(username=request.user, follow=look_user).exists():
                #request.userのfollowフィールドから閲覧中のユーザーを消去
                request.user.follow.remove(look_user)
                request.user.save()
                #フォローしていない場合
            else:
                #request.userのfollowフィールドから閲覧中のユーザーを追加
                request.user.follow.add(look_user)
                request.user.save()
                #直前のページにリダイレクト
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect("signup:login")





class SignupFollowListView(ListView):
    model = User
    template_name = "signup/signup_follow_list.html"

    def get_queryset(self, **kwargs):
        #閲覧中のユーザー取得
        visited_user_id = self.kwargs.get('users_id')
        visited_user = User.objects.get(id=visited_user_id)

        #自分のフォローを表示
        if visited_user == self.request.user:
            object_list = self.request.user.follow.all()

        #閲覧中のユーザーのフォローを表示
        else:
            object_list = visited_user.follow.all()
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


class SignupFollowerListView(ListView):
    model = User
    template_name = 'signup/signup_follow_list.html'

    def get_queryset(self, **kwargs):
        #閲覧中のユーザー取得
        visited_user_id = self.kwargs.get('users_id')
        visited_user = User.objects.get(id=visited_user_id)

        #閲覧中のユーザーのフォロワーを表示
        if visited_user == self.request.user:
            object_list = User.objects.filter(follow__username=self.request.user)
        #自分のフォロワーを表示
        else:
            object_list = User.objects.filter(follow__username=visited_user)
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



class SignupCreateView(LogoutRequiredMixin, FormView):
    form_class = CustomUserCreationForm
    template_name = "signup/signup_new.html"
    success_url = reverse_lazy("signup:login")


    def form_valid(self, form):
        button = self.request.POST.get("next")
        if button == "back":
            return render(self.request, "signup/signup_new.html", {"form":form})
        elif button == "confirm":
            return render(self.request, "signup/signup_regist.html", {"form":form})
        elif button == "regist":
            form.save()
            messages.success(self.request, "会員登録が完了しました。ユーザー名とパスワードを入力してログインしてください")
            return super().form_valid(form)
        else:
            return redirect("signup:login")
        return super().form_valid(form)


class SignupLoginView(LogoutRequiredMixin, LoginView):
    template_name = "login.html"

    def form_valid(self, form):
        messages.success(self.request, "ログインしました")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "ログインできませんでした。正しいパスワードとユーザー名を入力してください")
        return super().form_invalid(form)




class SignupDetailView(LoginRequiredMixin, TemplateView):
    template_name = "signup/signup_detail.html"
    login_url = "/signup/login/"


class SignupUpdateView(LoginRequiredMixin, OnlyMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = "signup/signup_update.html"
    success_url = reverse_lazy("eat:index")
    login_url = "/signup/login/"

    def form_valid(self, form):
        messages.success(self.request, "ユーザー情報を変更しました")
        return super().form_valid(form)


class SignupPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = "signup/signup_PasswordChange.html"
    success_url = reverse_lazy("eat:index")
    login_url = "/signup/login/"

    def form_valid(self, form):
        messages.success(self.request, "パスワードを変更しました")
        return super().form_valid(form)


"""
class SignupDeleteView(View):
    def get(self, *args, **kwargs):
        choise = self.request.GET.get("choise")
        print(choise)
        if choise == "delete":
            self.request.user.is_active = False
            self.request.user.save()
            SignupLogoutView()
        elif choise == "back":
            return redirect("signup:detail")
        else:
            return redirect("eat:index")
"""

class SignupDeleteView(LoginRequiredMixin, OnlyMixin, FormView):
    model = User
    form_class = CustomUpdateForm
    template_name = "signup/signup_delete.html"
    success_url = reverse_lazy("signup:new")
    login_url = "/signup/login/"

    def form_valid(self, form):
        self.request.user.is_active = False
        self.request.user.save()
        messages.success(self.request, "退会しました。再度アプリを利用するには会員登録が必要です")
        return super().form_valid(form)




"""
class SignupDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "signup/signup_delete.html"
    success_url = reverse_lazy("signup:new")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "退会しました。再度アプリを利用するには会員登録が必要です")
        return super().delete(request, *args, **kwargs)
"""
