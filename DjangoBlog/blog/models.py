from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse


# Create your models here.

class User(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"


class Post(models.Model):
    """
    Represents a post in the blog.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(null=False, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    body = RichTextUploadingField(blank=True, null=False, default="")

    class Meta:
        ordering = ["-created_on"]
