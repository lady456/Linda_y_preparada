from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from .forms import RegistroUsuarioForm
from .models import registro
# Create your views here.

def inicio(request):
        return render(request, 'paginas/inicio.html')
def citas(request):
        return render(request, 'paginas/citas.html')
def login(request):
        registros=registro.objects.all()
        data={'registros':registros}
        return render(request, 'paginas/login.html', data)
def confirmacion(request):
        return render(request, 'paginas/confirmacion.html')

def formulario(request):
        if request.method == 'POST':
                form = RegistroUsuarioForm(request.POST)
                if form.is_valid():
                        user = form.save()
                        return redirect('login') # Redirigir al login
        else:
                form = RegistroUsuarioForm()
        return render(request, 'usuarios/formulario.html', {'form': form})

def mis_citas(request):
        return render(request, 'usuarios/mis_citas.html')

def verificacion(request):
        return render(request, 'usuarios/verificacion.html' )    