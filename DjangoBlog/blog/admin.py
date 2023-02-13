from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, Post, Category


# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ["email", "username"]


class PostAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
    list_display = ('title',)
    prepopulated_fields = {
        'slug': ('title',),
    }


admin.site.register(User, CustomUserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
