from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('article/<int:article_id>/comment/', views.add_comment, name='add_comment'),
    path('article/<int:article_id>/comment/ajax/', views.add_comment_ajax, name='add_comment_ajax'),
    path('comment/ajax/<int:comment_id>/<str:action>/', views.moderate_comment_ajax, name='moderate_comment_ajax'),
    path('', views.article_list, name='home'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('category/<slug:slug>/', views.article_by_category, name='article_by_category'),
    path('tag/<slug:slug>/', views.article_by_tag, name='article_by_tag'),
    path('subscribe/', views.toggle_subscription, name='toggle_subscription'),
    path('article/<int:article_id>/rate/', views.rate_article, name='rate_article'),
    path('announcements/', views.announcement_list, name='announcement_list'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    path('article/create/', views.create_article, name='article_create'),








]


