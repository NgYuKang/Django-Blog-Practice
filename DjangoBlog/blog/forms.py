from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _

from .models import User, Comment, Post, Category


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "email")


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)
        labels = {
            'comment': _('Your comment'),
        }


class PostForm(forms.ModelForm):
    category = forms.CharField(max_length=50)

    def save(self, commit=True):
        category, created = Category.objects.get_or_create(name=self.cleaned_data['category'])
        self.instance.category = category
        return super().save(commit)

    class Meta:
        model = Post
        fields = ('title', 'body',)
