# shop/forms.py
# This file defines forms for user input in the shop app.
# Forms handle validation and make it easy to render input fields in templates.

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from shop.models import Product

class NewUserForm(UserCreationForm):
    """
    A registration form for new users.
    Inherits from Django's UserCreationForm and adds an email field.
    Fields:
      - username: The user's chosen username.
      - email: The user's email address.
      - password1: The user's password.
      - password2: Password confirmation.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class ProductForm(forms.ModelForm):
    """
    A form for staff to add new products to the shop.
    Only staff can use this form (enforced in the view).
    """
    class Meta:
        model = Product
        fields = ["name", "slug", "description", "price", "image", "category"] 