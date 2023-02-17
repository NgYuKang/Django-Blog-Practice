from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from django.template.defaultfilters import slugify


# Create your models here.

class SingletonModel(models.Model):

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    class Meta:
        abstract = True

class User(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(primary_key=True, max_length=100, unique=True, blank=False)

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

    def save(self, *args, **kwargs):
        if not self.pk or self._state.adding or self.title != Post.objects.get(pk=self.pk).title:
            self.slug = slugify(self.title)
        i = 1
        while Post.objects.filter(slug=self.slug).exists():
            self.slug = "-".join([slugify(self.title), str(i)])
            i += 1
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={
            'slug': self.slug
        })


class Comment(models.Model):
    """
    Represents a comment of a post
    """
    comment = models.TextField(verbose_name="Comment")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on", ]

class AboutPageBody(SingletonModel):
    body = RichTextUploadingField(blank=True, null=True)

    class Meta:
        verbose_name = "About Page"