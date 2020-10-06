from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
 
ALERTS = (
	("primary", "Blue"), # Key, Value
	("secondary", "Grey"),
	("danger", "Red"),
	("info", "Sky Blue"),
	("success", "Green"),
	("warning", "Yellow"),
	("dark", "Black"), 
	)
class Category(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	name = models.CharField(null=True, max_length=100, verbose_name="Category Name")
	color = models.CharField(null=True, max_length=50, choices=ALERTS)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = "Categories"

	def get_absolute_url(self):
		return reverse("cat", kwargs={ "pk": self.pk, "name" : self.name})

class Todo(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	name = models.CharField(null=True, max_length=300, verbose_name="To-Do Name", help_text="Please Type your Todo")	
	description = models.TextField(null=True, verbose_name="To-Do Description", blank=True, help_text="Optional")	
	category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True, blank=True, help_text="Optional")
	start_date = models.DateTimeField(auto_now_add=True, null=True)
	end_date = models.DateField(null=True, blank=True,  help_text="Optional: Type this if you want this todo to expire")
	expired = models.BooleanField(null=True, default=False)
	completed = models.BooleanField(null=True, default=False, verbose_name="Completed Todo", help_text="Optional: Only use this when you have completed your todo!")

	def __str__(self):
		return self.name

	class Meta:
		ordering = ["-start_date"]