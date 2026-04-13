from datetime import datetime, timedelta
import json
import random
from django.http import JsonResponse

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from django.core.mail import send_mail
from django.contrib import messages

from .forms import (
    RegistroUsuarioForm,
    CitaForm,
    ReprogramarCitaForm,
    PasswordResetRequestForm,
    PasswordResetCodeForm,
    NoAtendidaForm,
    CrearAdministradorForm,
)
from .models import Cita, PasswordResetCode

# Create your views here.

def _generate_reset_code():
    return f"{random.randint(100000, 999999)}"


def _send_reset_code(user):
    code = _generate_reset_code()
    PasswordResetCode.objects.create(user=user, code=code)
    subject = 'Código de recuperación de contraseña'
    message = (
        f'Hola {user.username},\n\n'
        f'Usa este código para restablecer tu contraseña: {code}\n'
        'El código es válido por 2 minutos.\n\n'
        'Si no usas el código, vuelve a solicitar uno nuevo.\n'
    )
    send_mail(subject, message, None, [user.email])

class CustomLoginView(LoginView):
    template_name = 'paginas/login.html'

    def get_success_url(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return reverse_lazy('administrador')
        return reverse_lazy('mis_citas')


def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email__iexact=email)
            _send_reset_code(user)
            request.session['password_reset_email'] = email
            messages.success(request, 'Se ha enviado un código de verificación a tu correo. Tiene 2 minutos de validez.')
            return redirect('password_reset_verify')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'usuarios/password_reset_request.html', {'form': form})


def password_reset_verify(request):
    email = request.session.get('password_reset_email')
    if not email:
        return redirect('password_reset_request')

    if request.method == 'POST' and request.POST.get('resend'):
        user = User.objects.get(email__iexact=email)
        _send_reset_code(user)
        messages.success(request, 'Se ha reenviado un nuevo código a tu correo.')
        return redirect('password_reset_verify')

    if request.method == 'POST':
        form = PasswordResetCodeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            code = form.cleaned_data['code']
            try:
                user = User.objects.get(email__iexact=email)
            except User.DoesNotExist:
                form.add_error('email', 'Correo no encontrado.')
            else:
                code_obj = PasswordResetCode.objects.filter(user=user, code=code, used=False).order_by('-created_at').first()
                if not code_obj:
                    form.add_error('code', 'Código inválido o ya usado.')
                elif code_obj.is_expired():
                    form.add_error('code', 'El código expiró. Solicita uno nuevo.')
                else:
                    code_obj.used = True
                    code_obj.save()
                    request.session['password_reset_user_id'] = user.id
                    return redirect('password_reset_confirm')
    else:
        form = PasswordResetCodeForm(initial={'email': email})

    return render(request, 'usuarios/password_reset_verify.html', {'form': form, 'email': email})


def password_reset_confirm(request):
    user_id = request.session.get('password_reset_user_id')
    if not user_id:
        return redirect('password_reset_request')

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            Cita.objects.filter(usuario=user).delete()
            auth_login(request, user)
            request.session.pop('password_reset_user_id', None)
            request.session.pop('password_reset_email', None)
            messages.success(request, 'Tu contraseña se actualizó. Las citas previas se borraron y ahora entras como un usuario nuevo.')
            return redirect('mis_citas')
    else:
        form = SetPasswordForm(user)

    return render(request, 'usuarios/password_reset_confirm.html', {
        'form': form,
        'user': user,
    })


def inicio(request):
    return render(request, 'paginas/inicio.html')


def _get_cita_for_action(request, cita_id):
    if request.user.is_superuser:
        return get_object_or_404(Cita, id=cita_id)
    return get_object_or_404(Cita, id=cita_id, usuario=request.user)


def _can_modify_cita(cita):
    cita_datetime = datetime.combine(cita.fecha, cita.hora)
    return cita_datetime - datetime.now() >= timedelta(hours=3)


@login_required
def confirmacion(request):
    servicio = request.GET.get('servicio')
    fecha = request.GET.get('fecha')
    hora = request.GET.get('hora')

    contexto = {
        'servicio': servicio,
        'fecha': fecha,
        'hora': hora,
    }

    return render(request, 'paginas/confirmacion.html', contexto)


def formulario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('citas')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'usuarios/formulario.html', {'form': form})


@login_required
def mis_citas(request):
    citas = Cita.objects.filter(usuario=request.user).order_by('-fecha', '-hora')
    return render(request, 'usuarios/mis_citas.html', {'citas': citas})


@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='login')
def administrador(request):
    profesional_filter = request.GET.get('profesional', '')

    # Base querysets
    citas_pendientes = Cita.objects.filter(estado='PENDIENTE').select_related('usuario')
    citas_reprogramadas = Cita.objects.filter(estado='REPROGRAMADA').select_related('usuario')
    citas_canceladas = Cita.objects.filter(estado='CANCELADA').select_related('usuario')
    citas_atendidas = Cita.objects.filter(estado='ATENDIDA').select_related('usuario')

    # Si es staff pero no superuser, filtrar solo sus citas
    if request.user.is_staff and not request.user.is_superuser:
        profesional_filter = request.user.username
        citas_pendientes = citas_pendientes.filter(profesional=profesional_filter)
        citas_reprogramadas = citas_reprogramadas.filter(profesional=profesional_filter)
        citas_canceladas = citas_canceladas.filter(profesional=profesional_filter)
        citas_atendidas = citas_atendidas.filter(profesional=profesional_filter)
    elif profesional_filter:
        citas_pendientes = citas_pendientes.filter(profesional=profesional_filter)
        citas_reprogramadas = citas_reprogramadas.filter(profesional=profesional_filter)
        citas_canceladas = citas_canceladas.filter(profesional=profesional_filter)
        citas_atendidas = citas_atendidas.filter(profesional=profesional_filter)

    # Ordenar
    citas_pendientes = citas_pendientes.order_by('fecha', 'hora')
    citas_reprogramadas = citas_reprogramadas.order_by('fecha', 'hora')
    citas_canceladas = citas_canceladas.order_by('-fecha', '-hora')
    citas_atendidas = citas_atendidas.order_by('-fecha', '-hora')

    contexto = {
        'citas_pendientes': citas_pendientes,
        'citas_reprogramadas': citas_reprogramadas,
        'citas_canceladas': citas_canceladas,
        'citas_atendidas': citas_atendidas,
        'profesional_filter': profesional_filter,
        'profesionales': Cita.PROFESIONAL_CHOICES,
        'es_superuser': request.user.is_superuser,
    }
    return render(request, 'sistema/administrador.html', contexto)


@user_passes_test(lambda u: u.is_superuser)
def crear_administrador(request):
    if request.method == 'POST':
        form = CrearAdministradorForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Administrador {user.username} creado exitosamente. Se cerrará la sesión para iniciar con el nuevo administrador.')
            auth_login(request, user)  # Iniciar sesión con el nuevo admin
            return redirect('administrador')
    else:
        form = CrearAdministradorForm()
    return render(request, 'sistema/crear_administrador.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def marcar_atendida(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    if cita.estado in ['PENDIENTE', 'CONFIRMADA', 'REPROGRAMADA']:
        cita.estado = 'ATENDIDA'
        cita.save()
        messages.success(request, f'La cita de {cita.usuario.username} ha sido marcada como atendida.')
    else:
        messages.error(request, 'Esta cita no puede ser marcada como atendida.')
    return redirect('administrador')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def marcar_no_atendida(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    if request.method == 'POST':
        form = NoAtendidaForm(request.POST)
        if form.is_valid():
            cita.estado = 'CANCELADA'  # O quizás un estado separado, pero por ahora usamos CANCELADA
            cita.descripcion_no_atendida = form.cleaned_data['descripcion']
            cita.save()
            messages.success(request, f'La cita de {cita.usuario.username} ha sido cancelada con descripción.')
            return redirect('administrador')
    else:
        form = NoAtendidaForm()
    return render(request, 'sistema/no_atendida.html', {'form': form, 'cita': cita})


def verificacion(request):
    return render(request, 'usuarios/verificacion.html')


@login_required
def cancelar_cita(request, cita_id):
    cita = _get_cita_for_action(request, cita_id)
    if not _can_modify_cita(cita):
        messages.error(request, 'No puedes cancelar una cita con menos de 3 horas de anticipación.')
        return redirect('administrador' if request.user.is_superuser else 'mis_citas')

    cita.estado = 'CANCELADA'
    cita.save()
    messages.success(request, 'La cita ha sido cancelada correctamente.')
    return redirect('administrador' if request.user.is_superuser else 'mis_citas')


@login_required
def reprogramar_cita(request, cita_id):
    cita = _get_cita_for_action(request, cita_id)
    if not _can_modify_cita(cita):
        messages.error(request, 'No puedes reprogramar una cita con menos de 3 horas de anticipación.')
        return redirect('administrador' if request.user.is_superuser else 'mis_citas')

    if request.method == 'POST':
        form = ReprogramarCitaForm(request.POST, instance=cita)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.estado = 'REPROGRAMADA'
            cita.save()
            messages.success(request, 'La cita ha sido reprogramada correctamente.')
            return redirect('administrador' if request.user.is_superuser else 'mis_citas')
    else:
        form = ReprogramarCitaForm(instance=cita)

    return render(request, 'paginas/reprogramar.html', {'form': form, 'cita': cita})


@login_required
def citas(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.usuario = request.user
            cita.save()
            return redirect('mis_citas')
    else:
        form = CitaForm()
    
    # Establecer fecha mínima como hoy
    from datetime import datetime
    today = datetime.now().date()
    form.fields['fecha'].widget.attrs['min'] = str(today)
    
    return render(request, 'paginas/citas.html', {'form': form})


@login_required
def obtener_horas_disponibles(request):
    """Endpoint AJAX que retorna las horas disponibles para un profesional en una fecha"""
    profesional = request.GET.get('profesional')
    fecha = request.GET.get('fecha')
    
    if not profesional or not fecha:
        return JsonResponse({'error': 'Faltan parámetros'}, status=400)
    
    try:
        # Obtener horas disponibles usando el método estático del formulario
        horas_disponibles = CitaForm.get_horas_disponibles(profesional, fecha)
        return JsonResponse({
            'horas': horas_disponibles,
            'profesional': profesional,
            'fecha': fecha
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


