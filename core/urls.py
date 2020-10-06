from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name="index"),
	path('todo/@<user>/<pk>/', views.todoPage, name="todo"),
	path('category/', views.category, name="category"),
	path('category/<pk>/<name>/', views.categoryPage, name="cat"),
	path('search/', views.search, name="search"),

	path('createTodo/', views.createTodo, name="todo-create" ),
	path('updateTodo/<pk>/', views.updateTodo, name="todo-update" ),
	path('deleteTodo/<pk>/', views.TodoDelete.as_view(), name="todo-delete"),

	path('createCategory/', views.CategoryCreate.as_view(), name="category-create" ),
	path('updateCategory/<pk>/', views.CategoryUpdate.as_view(), name="category-update" ),
	path('deleteCategory/<pk>/', views.CategoryDelete.as_view(), name="category-delete"),

	path('register/', views.register, name="register"),
	path('login/', views.signin, name="login"),
	path('logout/', views.signout, name="logout"),
	path('profile/', views.userProfile, name="profile"),
]