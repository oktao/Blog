from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from .forms import CommentForm, ArticleForm, CustomUserCreationForm
from .models import Article, Category, Tag


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

def logout_user(request):
    logout(request)
    return redirect('home')


def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id, status='published')
    form = CommentForm()

    return render(request, 'core/article_detail.html', {
        'article': article,
        'comment_form': form
    })


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
    return render(request, 'core/article_list.html', {
        'articles': articles,
    })

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

@login_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            form.save_m2m()  # для тегів
            return redirect('home')
    else:
        form = ArticleForm()
    return render(request, 'core/create_article.html', {'form': form})



