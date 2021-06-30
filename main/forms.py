from .models import Movie
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, ImageField, FileInput
from .models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_pic'].widget.clear_checkbox_label = 'Clear'
        self.fields['profile_pic'].widget.initial_text = "Current profile picture \n"
        self.fields['profile_pic'].widget.input_text = "Change profile picture \n"
