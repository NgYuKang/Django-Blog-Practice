from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('posts/<slug:slug>', views.PostDetailView.as_view(), name='post-detail'),
    path('accounts/signup', views.RegisterView.as_view(), name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),

    path('posts/create/', views.PostCreateView.as_view(), name='create-post'),
    path('posts/<slug:slug>/create-comment', views.CommentCreateView.as_view(), name='create-comment'),
    path('posts/<slug:slug>/delete-comment/<int:pk>', views.CommentDeleteView.as_view(), name='delete-comment'),
]
