from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db import IntegrityError
from django.utils import timezone
from .forms import TaskForm
from .models import Task

# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        print("Enviando formulario")
        return render(request, 'signup.html', {
            'form': UserCreationForm()
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            #Registrando usuario
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('task')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm(),
                    "error": "Usuario ya existe"
                })
            
        else:
            return render(request, 'signup.html', {
                'form': UserCreationForm(),
                "error": "Contraseñas no coinciden"
            })

@login_required        
def task(request):
    tasks = Task.objects.filter(user=request.user, date_completed__isnull=True)
    tasks_completed = Task.objects.filter(user=request.user, date_completed__isnull=False).order_by('-date_completed')
    return render(request, 'task.html', {'tasks': tasks, 'tasks_completed': tasks_completed})

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm()
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('task')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm(),
                "error": "Por favor ingrese datos válidos"
            })

def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm()
        })
    else:
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm(),
                "error": "Nombre de usuario o contraseña incorrectos"
            })
        else:
            login(request, user)
            return redirect('task')

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        try:
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                return redirect('task')
        except ValueError:
            form = TaskForm(request.POST, instance=task)
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': 'Error al actualizar la tarea. Por favor, ingrese datos válidos.'})
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_detail.html', {'task': task, 'form': form})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        if task.date_completed:
            task.date_completed = None
        else:
            task.date_completed = timezone.now()
        task.save()
    return redirect('task')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
    return redirect('task')

