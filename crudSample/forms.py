from django import forms
from .models import Post

# Create your models here.
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields =['title','body','image']

class PostSearchForm(forms.Form):
    search_word = forms.CharField(label='Search Word')

