from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView 
from django.urls import reverse_lazy

from . import models, forms
# Create your views here.
class PostListView(ListView):
    model = models.Post
    fields = "__all__"
    queryset = models.Post.objects.filter(active=True).order_by("-date_updated")

class PostDetailView(DetailView):
    model = models.Post

class PostCreateView(CreateView):
    form_class = forms.PostForm
    template_name = "forum/post_form.html"
    success_url = reverse_lazy("forum:post_list")

class PostUpdateView(UpdateView):
    form_class = forms.PostForm
    queryset = models.Post.objects.all()
    success_url = reverse_lazy("forum:post_list")

class PostDeleteView(DeleteView):
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(models.Post, id = kwargs["pk"])
        post.active = False
        post.save()
        
        return redirect("forum:post_list")
