from django.forms import ModelForm, TextInput, Textarea, SelectMultiple, DateInput, ClearableFileInput, PasswordInput
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class PostAddForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title","slug","text","tag"]
        widgets = {
            'title': TextInput(attrs={"class":"form-control"}),
            'slug': TextInput(attrs={"class":"form-control"}),
            "text": Textarea(attrs={"class": "form-control"}),
            "tag": SelectMultiple(attrs={"class":"form-control"})
        }
    def clean_slug(self):
        new_slug = self.cleaned_data["slug"].lower()
        if Post.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError("This slug already exist!")
        return new_slug



class TagAddForm(ModelForm):
    class Meta:
        model = Tag
        fields = ["title","slug"]
        widgets = {
            "title": TextInput(attrs={"class":"form-control"}),
            "slug": TextInput(attrs={"class":"form-control"}),
        }
    def clean_slug(self):
        new_title = self.cleaned_data['title'].lower()
        new_slug = self.cleaned_data['slug'].lower()
        if new_title == "add":
            raise ValidationError("You can't create Tag with this title!")
        if new_slug == "add" :
            raise ValidationError("You can't create Tag with this slug!")
        if Tag.objects.filter(title__iexact=new_title).count():
            raise ValidationError("Tag with this title already exist!")
        if Tag.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError("Tag with this slug already exist!")
        return new_slug


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": TextInput(attrs={"class":"form-control"})
        }


#temporarily account stuff here -_-
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name","last_name","email"]
        widgets = {
            "first_name": TextInput(attrs={"class": "form-control"}),
            "last_name": TextInput(attrs={"class": "form-control"}),
            "email": TextInput(attrs={"class": "form-control"}),
        }


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["bio","birth_date","pic"]
        widgets = {
            "bio": TextInput(attrs={"class": "form-control"}),
            "birth_date": DateInput(format=('%d-%m-%Y'),attrs={"class": "form-control"}),
            "pic": ClearableFileInput(attrs={"class": "form-control-file"}),
        }