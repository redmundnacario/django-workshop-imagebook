from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView 
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin, 
    UserPassesTestMixin,
    PermissionRequiredMixin,
)
from . import models, forms
from django.http import HttpResponseForbidden

#from django.http.response import HttpResponse
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import models as auth_models
from django.http import HttpResponseForbidden


"""
    # for function based view:
    #
    #from django.contrib.auth.decorators import login_required
    #@login_required        
"""
"""
    # function based view
    from django.contrib.auth.decorators import permission_required

    @permission_required("forum.view_post")
    def permission_on_function_based_view(request):
        return render(request, "forum/post_list.html", {})
"""

def handle_403(request, exception):
    return HttpResponse("Permission denied (error 403)", status=403)

def handle_404(request, exception):
    return HttpResponse("Di ko makita ang page (error 404)", status=404)

#    response = render(request, "404.html", {})
#    response.status_code = 404
#    return response

class PostListView( ListView):
    model = models.Post
    fields = "__all__"
    queryset = models.Post.objects.filter(active=True).order_by("-date_updated")
    permission_required = ("forum.view_post",)

    #def get(self, request, *args, **kwargs):
    #    if not request.user.has_perm("forum.view_post"):
    #        return HttpResponseForbidden("You are not allowed to do that")
    #    
    #    return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["user"] = self.request.user

        return context

class PostDetailView(DetailView):
    model = models.Post
    #queryset = models.Post.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.get_object().author == self.request.user or self.request.user.is_superuser:
            context["hide_button"] = False
        else :
            context["hide_button"] = True
        print(self.get_object().author, self.request.user, context)
        return context

class PostCreateView(CreateView):
    form_class = forms.PostForm
    template_name = "forum/post_form.html"
    success_url = reverse_lazy("forum:post_list")
    
    def _is_banned(self, request):
        status = request.user.groups.filter(name="Banned").exists()
        #status = request.user in auth_models.Group.objects.get(name="Banned").user_set.all()
        if status:
            return HttpResponseForbidden("You are currently banned in this social website.")

    def get(self, request, *args, **kwargs):
        status = self._is_banned(request)
        if status:
            return status

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        status = self._is_banned(request)
        if status:
            return status
        
        instance = models.Post()
        form = self.form_class(request.POST, instance=instance)
        if form.is_valid():
            if request.user.is_authenticated:
                instance.author = request.user

            form.save()

            return redirect(self.success_url)
        
        return render(request, self.template_name, {"form": form})

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

class PostDeleteView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        status = self._is_banned(request)
        if status:
            return status

        testimonial = get_object_or_404(models.Post, id=kwargs["pk"])
        testimonial.active = False
        testimonial.save()

        return redirect("forum:post_list")