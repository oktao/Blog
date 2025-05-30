from django import forms
from .models import Comment
from .models import Rating

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['value']
        widgets = {
            'value': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)])
        }
        labels = {
            'value': 'Ваша оцінка:'
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
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

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User  # твоя кастомна модель

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')  # додай, що потрібно


from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'category', 'tags', 'status']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }



