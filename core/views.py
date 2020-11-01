from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import *
from .models import *


# Home Page
@login_required(login_url='login')  # User must be authenticated before access to this page
def index(request):
    todos = Todo.objects.order_by("-start_date").filter(user=request.user, expired=False,
                                                        completed=False)  # Unexpired, Uncompleted Todo
    expired_todo = Todo.objects.order_by("-start_date").filter(user=request.user, expired=True)  # Expired Todo
    completed_todo = Todo.objects.order_by("-start_date").filter(user=request.user, expired=False,
                                                                 completed=True)  # Completed Todo
    frontend = {  # Passing Models to Frontend
        "todos": todos,
        "completed_todo": completed_todo,
        "expired_todo": expired_todo,
    }
    return render(request, 'core/index.html', frontend)


# Page for a specific todo
def todoPage(request, user, pk):
    # If Todo Object Exist Show Else Spit Error
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    frontend = {
        "todo": todo,
    }
    return render(request, 'core/todo.html', frontend)


# Summary of Categories for a User
def category(request):
    categories = Category.objects.filter(user=request.user)  # Sort Category by Authenticated User
    frontend = {
        "categories": categories,
    }
    return render(request, 'core/category.html', frontend)


# Single Page for Specific Category
def categoryPage(request, pk, name):
    category = get_object_or_404(Category, pk=pk, name=name)
    frontend = {
        "category": category,
    }
    return render(request, 'core/category-page.html', frontend)


# Search Functionality
def search(request):
    # Create a Variable and Store All Todo Objects in it
    query = Todo.objects.order_by("-start_date").filter(user=request.user, expired=False)

    # Keyword is the search name from the front-end
    if "keyword" in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            # Sort Keyword to match Query
            query = query.filter(description__icontains=keyword) or query.filter(name__icontains=keyword)
    keyword = request.GET['keyword']

    frontend = {
        "keyword": keyword,
        "query": query,
    }
    return render(request, 'core/search.html', frontend)


# Creating Todo Application
def createTodo(request):
    if request.method == "POST":  # If Request Method is POST
        # Save the User and Form Data into Form
        form = TodoForm(request.user, request.POST)
        # Check If Form is Valid
        if form.is_valid():
            todo = form.save()
            todo.user = request.user  # Save Authenticated User as User of Form
            todo.save()  # Save Form
            messages.success(request, "Todo successfully created!")  # Send a Success Message
            return redirect('todo', user=request.user, pk=todo.pk)  # Redirect to Single Todo Page
    else:
        form = TodoForm(request.user)
    frontend = {"form": form}
    return render(request, 'core/todo-create.html', frontend)


# Updating Todo App
def updateTodo(request, pk):
    todo = Todo.objects.get(pk=pk)  # Find Todo Object that matches id of url
    if request.method == "POST":
        #  When Form Id is found, Update existing fields
        form = TodoForm(user=request.user, data=request.POST, instance=todo)
        if form.is_valid():
            bar = form.save()
            bar.save()
            messages.success(request, "Todo successfully updated")
            return redirect('todo', user=request.user, pk=bar.pk)  # Redirect to Single Todo Page
    else:
        form = TodoForm(user=request.user, instance=todo)
    frontend = {
        "form": form
    }
    return render(request, "core/todo-update.html", frontend)


# Deleting the todo, Login is Required
class TodoDelete(LoginRequiredMixin, DeleteView):
    model = Todo
    success_message = "Todo was deleted successfully!"
    success_url = reverse_lazy('index')  # Redirects to this page
    template_name = "core/app_delete.html"

    # Method to Activate "success_message" variable above
    def delete(self, request, *args, **kwargs):
        messages.info(self.request, self.success_message)
        return super(TodoDelete, self).delete(request, *args, **kwargs)


# Creating a New Category Object
class CategoryCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name', "color"]
    template_name = "core/category-create.html"
    success_message = "Category was created successfully!"

    # Validates Form
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# Updating a Category
class CategoryUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Category
    fields = ['name', "color"]
    template_name = "core/category-update.html"
    success_message = "Category was updated successfully!"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# Deleting a Category
class CategoryDelete(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('index')
    template_name = "core/app_delete.html"
    success_message = "Category was deleted successfully!"

    def delete(self, request, *args, **kwargs):
        messages.info(self.request, self.success_message)
        return super(CategoryDelete, self).delete(request, *args, **kwargs)


# Registration Form for User
def register(request):
    form = UserForm()  # Creating an instance of the form
    if request.method == "POST":
        user = UserForm(request.POST)  # Saving Data into form
        if user.is_valid():
            user.save()
            username = user.cleaned_data['username']  # Collecting Username of the Newly Created user
            messages.success(request, f"Welcome New User {username}")  # Sending message
            return redirect("login")
        else:
            # Sending any  error to user
            for msg in user.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
    frontend = {"form": form}
    return render(request, "core/register.html", frontend)


# Login Form/ Page for User
def signin(request):
    if request.method == "POST":
        username = request.POST["username"]  # Collect Username from frontend
        password = request.POST["password"]  # Collect password from frontend
        user = authenticate(request, username=username, password=password)  # Verify User
        if user is not None:  # If User Exists
            login(request, user)  # Login User
            messages.success(request, f"Welcome {username} !")
            return redirect("index")
        else:
            messages.error(request, "Invalid Credentials")
    return render(request, "core/login.html")


# Sign Out USer
def signout(request):
    if request.method == "POST":
        logout(request)
        messages.info(request, "Succesfully Logged Out, Love to see you again!!")
        return redirect("login")


# Page for User to Change their Names etc
def userProfile(request):
    user = request.user
    form = UserProfileForm(instance=user)
    frontend = {"form": form}

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid:
            form.save()
            messages.success(request, f"Your Profile was successfully updated, {user}")
    return render(request, "core/settings.html", frontend)
