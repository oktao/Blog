from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.article_list, name='home'),

    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),

    path('article/create/', views.create_article, name='article_create'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('article/<int:article_id>/comment/', views.add_comment, name='add_comment'),

    path('category/<slug:slug>/', views.article_by_category, name='article_by_category'),
    path('tag/<slug:slug>/', views.article_by_tag, name='article_by_tag')
    
]