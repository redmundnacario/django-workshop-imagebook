from django.contrib import admin

# Register your models here.
from . import models


# @admin.register(models.User)
# class UserAdmin(admin.ModelAdmin):
#     pass

@admin.register(models.Post)
class PostsAdmin(admin.ModelAdmin):
    pass