from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.db import IntegrityError

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
            print("Contraseñas coinciden")
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
        
def task(request):
    return render(request, 'task.html')

def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html')
    else:
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is None:
            return render(request, 'signin.html', {
                "error": "Nombre de usuario o contraseña incorrectos"
            })
        else:
            login(request, user)
            return redirect('task')
