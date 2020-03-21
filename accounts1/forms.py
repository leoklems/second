from django import forms
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms import ModelForm, Textarea, TextInput, ClearableFileInput
from .models import Order, Customer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        field = '__all__'
        exclude = ['user']
class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'product', 'status']
        #fields = "__all__"

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']