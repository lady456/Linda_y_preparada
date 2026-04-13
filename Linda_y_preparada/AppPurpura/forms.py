from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import Cita
from datetime import datetime, time

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(label="Correo electrónico", required=True)
    verificacion_humano = forms.BooleanField(required=True, label="Verifica que eres un humano")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

class CrearAdministradorForm(UserCreationForm):
    email = forms.EmailField(label="Correo electrónico", required=True)
    verificacion_humano = forms.BooleanField(required=True, label="Verifica que eres un humano")
    nombre_profesional = forms.ChoiceField(
        choices=Cita.PROFESIONAL_CHOICES,
        label="Profesional",
        help_text="Selecciona la profesional que será administradora"
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean_nombre_profesional(self):
        nombre = self.cleaned_data['nombre_profesional']
        if User.objects.filter(username=nombre, is_staff=True).exists():
            raise forms.ValidationError(f'Ya existe un administrador para {nombre}.')
        return nombre

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True  # Marcar como staff
        user.username = self.cleaned_data['nombre_profesional']  # Usar el nombre de la profesional como username
        if commit:
            user.save()
        return user

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico registrado', required=True)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('No existe ningún usuario registrado con ese correo.')
        return email

class PasswordResetCodeForm(forms.Form):
    email = forms.EmailField(widget=forms.HiddenInput())
    code = forms.CharField(
        label='Código de verificación',
        min_length=6,
        max_length=6,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ingresa el código de 6 dígitos'
        })
    )

class CitaForm(forms.ModelForm):
    HORA_CHOICES = [
        (f'{hour:02d}:00', f'{hour}:00') for hour in range(7, 18)
    ]
    
    hora = forms.TimeField(
        widget=forms.Select(choices=HORA_CHOICES),
        input_formats=['%H:%M'],
    )
    
    class Meta:
        model = Cita
        fields = ['servicio', 'profesional', 'fecha', 'hora']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        hoy = datetime.now().date()
        if fecha.month != hoy.month or fecha.year != hoy.year:
            raise forms.ValidationError("Solo puedes agendar citas en el mes en curso.")
        if fecha < hoy:
            raise forms.ValidationError("La fecha no puede ser anterior a hoy.")
        return fecha

    def clean(self):
        """Validar que no exista una cita con el mismo profesional, fecha y hora"""
        cleaned_data = super().clean()
        profesional = cleaned_data.get('profesional')
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')

        if profesional and fecha and hora:
            # Buscar si existe una cita para este profesional, fecha y hora
            cita_existente = Cita.objects.filter(
                profesional=profesional,
                fecha=fecha,
                hora=hora,
                estado__in=['PENDIENTE', 'CONFIRMADA', 'REPROGRAMADA']  # No contar canceladas
            ).exists()
            
            if cita_existente:
                raise forms.ValidationError(
                    f"Lo sentimos, {profesional} no está disponible en esa fecha y hora. "
                    "Por favor, elige otra opción."
                )
        
        return cleaned_data
    
    @staticmethod
    def get_horas_disponibles(profesional, fecha):
        """Retorna las horas disponibles para un profesional en una fecha específica"""
        HORAS_DISPONIBLES = [f'{hour:02d}:00' for hour in range(7, 18)]
        
        # Obtener horas ya reservadas para este profesional en esta fecha
        citas_reservadas = Cita.objects.filter(
            profesional=profesional,
            fecha=fecha,
            estado__in=['PENDIENTE', 'CONFIRMADA', 'REPROGRAMADA']
        ).values_list('hora', flat=True)
        
        # Convertir TimeField a string para comparación
        horas_ocupadas = [str(hora) for hora in citas_reservadas]
        
        # Retornar solo las horas disponibles
        horas_libres = [h for h in HORAS_DISPONIBLES if h not in horas_ocupadas]
        return horas_libres


class ReprogramarCitaForm(forms.ModelForm):
    HORA_CHOICES = [
        (f'{hour:02d}:00', f'{hour}:00') for hour in range(7, 18)
    ]

    hora = forms.TimeField(
        widget=forms.Select(choices=HORA_CHOICES),
        input_formats=['%H:%M'],
    )

    class Meta:
        model = Cita
        fields = ['fecha', 'hora']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }

class NoAtendidaForm(forms.Form):
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe brevemente por qué no se realizó la cita'}),
        label='Descripción',
        required=True
    )

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        hoy = datetime.now().date()
        if fecha.month != hoy.month or fecha.year != hoy.year:
            raise forms.ValidationError("Solo puedes agendar citas en el mes en curso.")
        if fecha < hoy:
            raise forms.ValidationError("La fecha no puede ser anterior a hoy.")
        return fecha
    
    def clean(self):
        """Validar que no exista otra cita con el mismo profesional, fecha y hora"""
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')
        
        # Obtener la cita que se está reprogramando
        cita_actual = self.instance
        profesional = cita_actual.profesional

        if fecha and hora:
            # Buscar si existe otra cita diferente para este profesional, fecha y hora
            cita_existente = Cita.objects.filter(
                profesional=profesional,
                fecha=fecha,
                hora=hora,
                estado__in=['PENDIENTE', 'CONFIRMADA', 'REPROGRAMADA']
            ).exclude(id=cita_actual.id).exists()
            
            if cita_existente:
                raise forms.ValidationError(
                    f"Lo sentimos, {profesional} no está disponible en esa fecha y hora."
                )
        
        return cleaned_data
