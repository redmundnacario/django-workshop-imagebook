from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView 
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from . import models, forms

# for function based view:
#
#from django.contrib.auth.decorators import login_required
#@login_required        


class PostListView(ListView):
    model = models.Post
    fields = "__all__"
    queryset = models.Post.objects.filter(active=True).order_by("-date_updated")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["user"] = self.request.user

        return context

class PostDetailView(DetailView):
    model = models.Post
    #queryset = models.Post.objects.filter(active=True)

class PostCreateView(CreateView):
    form_class = forms.PostForm
    template_name = "forum/post_form.html"
    success_url = reverse_lazy("forum:post_list")
    
    def post(self, request, *args, **kwargs):
        instance = models.Post()
        form = self.form_class(request.POST, instance=instance)
        if form.is_valid:
            if request.user.is_authenticated:
                instance.author = request.user

            form.save()

        return redirect(self.success_url)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = forms.PostForm
    queryset = models.Post.objects.all()
    success_url = reverse_lazy("forum:post_list")

    def test_func(self):
        return (
            self.get_object().author == self.request.user or
            self.request.user.is_superuser
        )

        #test1 = self.get_object().author == self.request.user
        #test2 = self.request.user.is_superuser
        #return any([test1, test2, test3, test4])

class PostDeleteView(View):
    def get(self, request, *args, **kwargs):
        testimonial = get_object_or_404(models.Post, id=kwargs["pk"])
        testimonial.active = False
        testimonial.save()

        return redirect("forum:post_list")