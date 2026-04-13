from django.http import HttpResponse

from django.shortcuts import render, redirect

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

def registro_usu(request):
        form = RegistroUsuarioForm(request.POST or None, request.FILES or None)
        if form.is_valid():
                form.save()
        return render(request, 'usuarios/registro_usu.html', {'form': form})

def verificacion(request):
        return render(request, 'usuarios/verificacion.html' )    