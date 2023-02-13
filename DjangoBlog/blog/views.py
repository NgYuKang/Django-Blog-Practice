from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy


# Create your views here.

class IndexView(TemplateView):
    template_name = "index.html"


class RegisterView(CreateView):
    template_name = "registration/signup.html"
    success_url = reverse_lazy('login')
    form_class = CustomUserCreationForm
