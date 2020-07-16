from django.contrib import admin
from django.urls import path
from signup.models import User
from .views import EatListView, EatDetailView, EatCreateView, EatUpdateView, EatDeleteView, EatTimeLineListView, EatUsersListView, EatFindListView, EatGoodUsersListView, good, EatQuoteDetailView, EatQuoteCreateView

app_name = "eat"

urlpatterns = [
    path('index/', EatListView.as_view(), name="index"),
    path('detail/<int:pk>/', EatDetailView.as_view(), name="detail"),
    path('create/', EatCreateView.as_view(), name="create"),
    path('update/<int:pk>/', EatUpdateView.as_view(), name="update"),
    path('delete/<int:pk>/', EatDeleteView.as_view(), name="delete"),
    path('timeline/', EatTimeLineListView.as_view(), name="timeline"),
    path('users/<int:users_id>/', EatUsersListView.as_view(), name="users"),
    path('find/', EatFindListView.as_view(), name="find"),
    path('<int:pk>/', good, name="good"),
    path('detail/quote/<int:pk>/', EatQuoteDetailView.as_view(), name="quote_detail"),
    path('create/quote/<int:pk>/', EatQuoteCreateView.as_view(), name="quote_create"),
    #path('<int:pk>', GoodUpdateView.as_view(), name = 'good')
    path('list/<int:users_id>/', EatGoodUsersListView.as_view(), name='good_users_list')

]
 
