from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, ListView, View, DeleteView, UpdateView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.http import HttpResponseRedirect

from django.db.models import Count

from .forms import CommentForm, PostForm
from .models import Post, Comment, Category


# Create your views here.

class IndexView(ListView):
    template_name = "index.html"
    model = Post
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('category')
        if query:
            return self.model.objects.filter(category=query)
        return self.model.objects.all()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(num_post=Count('post'))
        context['selected_category'] = self.request.GET.get('category', None)
        return context


class RegisterView(CreateView):
    template_name = "registration/signup.html"
    success_url = reverse_lazy('login')
    form_class = CustomUserCreationForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('index'))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'You have successfully registered for an account. Please log in below.')
        return response


class PostDetailView(ListView):
    model = Comment
    template_name = "post-detail.html"
    paginate_by = 5
    comment_form = CommentForm
    detail_view_obj_name = "post"

    object = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_object(self):
        # Get the id of the article via the link
        post_id = self.kwargs.get("slug")
        queryset = Post.objects.all()
        return get_object_or_404(queryset, slug=post_id)

    def get_queryset(self):
        return self.object.comment_set.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.detail_view_obj_name] = self.object
        context["comment_form"] = self.comment_form
        return context


class CommentCreateView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = self.request.user

            post_id = kwargs.get("slug")
            post = get_object_or_404(Post, slug=post_id)
            comment.post = post
            form.save(commit=True)

        return HttpResponseRedirect(reverse_lazy('post-detail', kwargs={
            "slug": kwargs.get("slug"),
        }))


class CommentDeleteView(UserPassesTestMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        return self.get_object().post.get_absolute_url()

    def test_func(self):
        return self.request.user == self.get_object().user


class PostDeleteView(UserPassesTestMixin, DeleteView):
    model = Post

    def get_success_url(self):
        return reverse_lazy('index')

    def test_func(self):
        return self.request.user == self.get_object().author or self.request.user.is_staff


class PostCreateView(UserPassesTestMixin, CreateView):
    model = Post
    form_class = PostForm
    context_object_name = "post"
    success_url = reverse_lazy('index')
    template_name = "post_create.html"

    def form_valid(self, form):
        post = form.save(commit=False)

        post.author = self.request.user
        post = form.save(commit=True)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={
            'slug': self.object.slug
        })

    def test_func(self):
        return self.request.user.is_staff


class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    context_object_name = "post"
    success_url = reverse_lazy('index')
    template_name = "post_edit.html"

    def form_valid(self, form):
        post = form.save(commit=False)

        post.author = self.request.user
        post = form.save(commit=True)
        return super().form_valid(form)

    def get_initial(self):
        initials = super().get_initial()
        initials["category"] = self.object.category
        return initials

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={
            'slug': self.object.slug
        })

    def test_func(self):
        return self.request.user.is_staff
