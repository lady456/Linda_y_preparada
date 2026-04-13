from django.http import HttpResponse

from django.shortcuts import render

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
        return render(request, 'usuarios/formulario.html')
