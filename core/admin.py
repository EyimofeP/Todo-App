from django.contrib import admin

from .models import *

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'name', 'color')
	list_display_link = ('id', 'name')
	list_filter = ('user',)
	list_per_page = 30

class TodoAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', "user",'category',"expired", "start_date", "end_date")
	list_editable = ("expired",)
	list_display_link = ('id', 'name')
	list_filter = ('user',)
	list_per_page = 50

admin.site.register(Category, CategoryAdmin)
admin.site.register(Todo, TodoAdmin) 