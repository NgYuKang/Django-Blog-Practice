from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib import messages


# Create your views here.

class IndexView(TemplateView):
    template_name = "index.html"


class RegisterView(CreateView):
    template_name = "registration/signup.html"
    success_url = reverse_lazy('login')
    form_class = CustomUserCreationForm

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'You have successfully registered for an account. Please log in below.')
        return response

