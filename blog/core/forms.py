from django import forms
from .models import Comment, Article
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Напишіть ваш коментар тут...',
                'rows': 3
            }),
        }
        labels = {
            'content': ''
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')  # додай, що потрібно

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'content', 'category', 'tags', 'status')
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }



