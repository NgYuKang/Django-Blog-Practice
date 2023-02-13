from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('accounts/signup', views.RegisterView.as_view(), name='signup'),
    path('accounts/', include('django.contrib.auth.urls'))
]