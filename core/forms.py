from django import forms
from django.forms import ModelForm

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Todo, Category

class UserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ["username","first_name","last_name","email","password1","password2"]
		help_texts = {
			"username": "Username should be more than 30 characters",
			"email": "We are just using this, incase you forget your password!",
			"first_name": "Enter your First Name",
			"last_name": "Enter your Last Name",
		}

class UserProfileForm(ModelForm):
	class Meta:
		model = User
		fields = "__all__"

class DateInput(forms.DateInput):
	input_type = "date"

class TodoForm(ModelForm):
	class Meta:
		model = Todo
		fields = ["id", "name", "category", "end_date", "description","completed"]
		widgets = {"end_date": DateInput()}

	def __init__(self, user, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["category"].queryset = Category.objects.filter(user=user)

	def form_valid(self,form):
		form.instance.user = self.request.user
		return super().form_valid(form)