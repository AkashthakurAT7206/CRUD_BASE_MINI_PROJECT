from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Todo
from .import forms
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
# Create your views here.

class TodoListView(ListView):
    model = Todo
    template_name = 'app/todo_list.html'
    context_object_name = 'todos'
    
class TodoCreateView(CreateView):
    model = Todo
    fields = ["title", "description", "completed", "due_date", "priority"]
    template_name = "app/todo_form.html"      # create/edit form
    success_url = reverse_lazy("todo-list")


class TodoUpdateView(UpdateView):
    model = Todo
    fields = ["title", "description", "completed", "due_date", "priority"]
    template_name = "app/todo_form.html"
    success_url = reverse_lazy("todo-list")
  
class TodoDeleteView(DeleteView):
    model = Todo
    template_name = "app/todo_confirm_delete.html"
    success_url = reverse_lazy("todo-list")    

