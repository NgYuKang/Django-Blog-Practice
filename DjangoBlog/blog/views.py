from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, ListView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Post


# Create your views here.

class IndexView(ListView):
    template_name = "index.html"
    model = Post
    context_object_name = "posts"
    paginate_by = 5


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
