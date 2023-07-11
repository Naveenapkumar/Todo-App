from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView

from .models import Task


# Create your views here.
class RegisterPage(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')
    def form_valid(self, form):
        user=form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterPage,self).form_valid(form)
class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields='__all__'
    redirect_authenticated_user = True
#to return user to task list page
    def get_success_url(self):
        return reverse_lazy('tasks')

class TaskList(LoginRequiredMixin,ListView):
    model= Task
    context_object_name = 'tasks'
    template_name = 'task_list.html'

    #to get tasklist differently for each users
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['tasks']=context['tasks'].filter(user=self.request.user)
        return context

class TaskDetail(LoginRequiredMixin,DetailView):
    model=Task
    template_name='task_detail.html'
    context_object_name = 'tasks'

class TaskCreate(LoginRequiredMixin,CreateView):
    model=Task
    fields = ['title', 'description', 'complete']
    template_name= 'task_create.html'
    success_url = reverse_lazy('tasks')
#    to prevent selecting multiple users while creating a task
    def form_valid(self, form):
        form.instance.user= self.request.user
        return super(TaskCreate,self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title','description','complete']
    template_name = 'task_create.html'
    success_url = reverse_lazy('tasks')

class TaskDelete(DeleteView):
    model=Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    template_name = 'task_confirm_delete.html'

