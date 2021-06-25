from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from . import views

urlpatterns = [

    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page=reverse_lazy("forum:post_list")), name="logout"),
    path("register", views.register, name="register"),

    # https://docs.djangoproject.com/en/3.0/topics/auth/default/#using-the-views    
    path("", include("django.contrib.auth.urls")),
]