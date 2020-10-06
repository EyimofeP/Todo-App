import datetime

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


@login_required(login_url='login')
def index(request):
    todos = Todo.objects.order_by("-start_date").filter(user=request.user, expired=False, completed=False)
    expired_todo = Todo.objects.order_by("-start_date").filter(user=request.user, expired=True)
    completed_todo = Todo.objects.order_by("-start_date").filter(user=request.user, expired=False, completed=True)
    frontend = {
        "todos": todos,
        "completed_todo": completed_todo,
        "expired_todo": expired_todo,
    }
    return render(request, 'core/index.html', frontend)


def todoPage(request, user, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    frontend = {
        "todo": todo,
    }
    return render(request, 'core/todo.html', frontend)


def category(request):
    categories = Category.objects.filter(user=request.user)
    frontend = {
        "categories": categories,
    }
    return render(request, 'core/category.html', frontend)


def categoryPage(request, pk, name):
    category = get_object_or_404(Category, pk=pk, name=name)
    frontend = {
        "category": category,
    }
    return render(request, 'core/category-page.html', frontend)


def search(request):
    query = Todo.objects.order_by("-start_date").filter(user=request.user, expired=False)

    if "keyword" in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            query = query.filter(description__icontains=keyword) or query.filter(name__icontains=keyword)
    keyword = request.GET['keyword']

    frontend = {
        "keyword": keyword,
        "query": query,
    }
    return render(request, 'core/search.html', frontend)


def createTodo(request):
    if request.method == "POST":
        form = TodoForm(request.user, request.POST)
        if form.is_valid():
            todo = form.save()
            todo.user = request.user
            todo.save()
            messages.success(request, "Todo successfully created!")
            return redirect('todo', user=request.user, pk=todo.pk)
    else:
        form = TodoForm(request.user)
        messages.error(request, "An Error occured, Try Again Later!!")
    frontend = {"form": form}
    return render(request, 'core/todo-create.html', frontend)


def updateTodo(request, pk):
    todo = Todo.objects.get(pk=pk)
    if request.method == "POST":
        form = TodoForm(user=request.user, data=request.POST, instance=todo)
        if form.is_valid():
            bar = form.save()
            bar.save()
            messages.success(request, "Todo successfully updated")
            return redirect('todo', user=request.user, pk=bar.pk)
    else:
        form = TodoForm(user=request.user, instance=todo)
    frontend = {
        "form": form
    }
    return render(request, "core/todo-update.html", frontend)


class TodoUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Todo
    form_class = TodoForm
    template_name = "core/todo-update.html"
    success_message = "Todo was updated successfully!"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TodoDelete(LoginRequiredMixin, DeleteView):
    model = Todo
    success_message = "Todo was deleted successfully!"
    success_url = reverse_lazy('index')
    template_name = "core/app_delete.html"

    def delete(self, request, *args, **kwargs):
        messages.info(self.request, self.success_message)
        return super(TodoDelete, self).delete(request, *args, **kwargs)


class CategoryCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name', "color"]
    template_name = "core/category-create.html"
    success_message = "Category was created successfully!"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CategoryUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Category
    fields = ['name', "color"]
    template_name = "core/category-update.html"
    success_message = "Category was updated successfully!"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CategoryDelete(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('index')
    template_name = "core/app_delete.html"
    success_message = "Category was deleted successfully!"

    def delete(self, request, *args, **kwargs):
        messages.info(self.request, self.success_message)
        return super(CategoryDelete, self).delete(request, *args, **kwargs)


def register(request):
    form = UserForm()
    if request.method == "POST":
        user = UserForm(request.POST)
        if user.is_valid():
            user.save()
            username = user.cleaned_data['username']
            messages.success(request, f"Welcome New User {username}")
            return redirect("login")
        else:
            for msg in user.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
    frontend = {"form": form}
    return render(request, "core/register.html", frontend)


def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {username} !")
            return redirect("index")
        else:
            messages.error(request, "Invalid Credentials")
    return render(request, "core/login.html")


def signout(request):
    if request.method == "POST":
        logout(request)
        messages.info(request, "Succesfully Logged Out, Love to see you again!!")
        return redirect("login")


def userProfile(request):
    user = request.user
    form = UserProfileForm(instance=user)
    frontend = {"form": form}

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid:
            form.save()
            messages.success(request, f"Your Profile was successfully updated, {user.first_name}")
    return render(request, "core/settings.html", frontend)
