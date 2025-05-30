from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Comment
from .forms import CommentForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponseForbidden
from .forms import RatingForm
from .models import Rating
from .models import Announcement
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


@login_required
def add_comment(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
            return redirect('article_detail', article_id=article.id)
    else:
        form = CommentForm()

    return render(request, 'core/article_detail.html', {
        'article': article,
        'form': form,
    })

from django.http import JsonResponse
from django.template.loader import render_to_string

@login_required
def add_comment_ajax(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()

            comments_html = render_to_string('core/partials/_comments.html', {'article': article})
            return JsonResponse({'success': True, 'comments_html': comments_html})
    return JsonResponse({'success': False})

@login_required
def moderate_comment_ajax(request, comment_id, action):
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user

    if user.is_superuser or comment.article.author == user:
        if action == 'approve':
            comment.is_approved = True
            comment.save()
        elif action == 'delete':
            comment.delete()

        # Повертаємо оновлений HTML блоку коментарів
        comments_html = render_to_string('core/partials/_comments.html', {'article': comment.article, 'user': user})
        return JsonResponse({'success': True, 'comments_html': comments_html})
    else:
        return JsonResponse({'success': False, 'error': 'Access denied'})
    
def article_list(request):
    articles = Article.objects.filter(status='published').order_by('-created_at')
    return render(request, 'article.html', {'articles': articles})

def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id, status='published')
    return render(request, 'core/article_detail.html', {'article': article})

from .models import Category, Tag

def article_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(category=category, status='published').order_by('-created_at')
    return render(request, 'core/article_list.html', {
        'articles': articles,
        'filter_title': f"Категорія: {category.name}"
    })

def article_by_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    articles = Article.objects.filter(tags=tag, status='published').order_by('-created_at')
    return render(request, 'core/article_list.html', {
        'articles': articles,
        'filter_title': f"Тег: {tag.name}"
    })

def article_list(request):
    articles = Article.objects.filter(status='published').order_by('-created_at')
    categories = Category.objects.all()
    tags = Tag.objects.all()
    return render(request, 'core/article_list.html', {
        'articles': articles,
        'categories': categories,
        'tags': tags
    })


@login_required
def toggle_subscription(request):
    subscription, created = subscription.objects.get_or_create(user=request.user)
    subscription.is_active = not subscription.is_active
    subscription.save()
    return redirect('home')


@login_required
def rate_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    rating, created = Rating.objects.get_or_create(user=request.user, article=article)

    if request.method == 'POST':
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            form.save()
            return redirect('article_detail', article_id=article.id)
    else:
        form = RatingForm(instance=rating)

    return render(request, 'core/article_detail.html', {
        'article': article,
        'rating_form': form,
    })

def article_list(request):
    articles = Article.objects.filter(status='published').order_by('-created_at')
    announcements = Announcement.objects.all()[:3]  # останні 3 оголошення
    categories = Category.objects.all()
    tags = Tag.objects.all()
    return render(request, 'core/article_list.html', {
        'articles': articles,
        'announcements': announcements,
        'categories': categories,
        'tags': tags
    })

def announcement_list(request):
    announcements = Announcement.objects.all()
    return render(request, 'core/announcement_list.html', {'announcements': announcements})




from .forms import CustomUserCreationForm  

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})


from .models import Subscription

from django.shortcuts import redirect

@login_required
def toggle_subscription(request):
    subscription, created = Subscription.objects.get_or_create(user=request.user)

    # просто перемикаємо статус
    subscription.is_active = not subscription.is_active
    subscription.save()

    return redirect('home')  

from django.contrib.auth.decorators import login_required
from .forms import ArticleForm
from .models import Article

@login_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            form.save_m2m()  # для тегів
            return redirect('article_detail', article.id)
    else:
        form = ArticleForm()
    return render(request, 'core/create_article.html', {'form': form})



