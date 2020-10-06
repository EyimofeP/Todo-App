from django import forms
from django.forms import ModelForm

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Todo, Category


# Form that Extends Users Default Registration Form
class UserForm(UserCreationForm):
    class Meta:
        model = User  # Model to Extend/ Inherit
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]  # Fields needed

        # Helpful Information given to users when completing form
        help_texts = {
            "username": "Username should be more than 30 characters",
            "email": "We are just using this, in case you forget your password!",
            "first_name": "Enter your First Name",
            "last_name": "Enter your Last Name",
        }


# Form for User Settings
class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = "__all__"


class DateInput(forms.DateInput):
    input_type = "date"


# Form for Todo
class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ["id", "name", "category", "end_date", "description", "completed"]
        widgets = {"end_date": DateInput()}

    # Sort Categories according to User
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(user=user)

    # Validates Form
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
