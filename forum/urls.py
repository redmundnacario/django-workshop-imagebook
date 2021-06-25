from django.urls import path

from . import views

app_name = "forum"

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("<int:pk>", views.PostDetailView.as_view(), name="post_detail"),
    path("post/create", views.PostCreateView.as_view(), name="post_create"),
    path("post/edit/<int:pk>", views.PostUpdateView.as_view(), name="post_edit"),
    path("post/delete/<int:pk>", views.PostDeleteView.as_view(), name="post_delete"),
]