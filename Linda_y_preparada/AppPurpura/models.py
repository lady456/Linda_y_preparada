from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class Cita(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('REPROGRAMADA', 'Reprogramada'),
        ('CANCELADA', 'Cancelada'),
        ('ATENDIDA', 'Atendida'),
    ]
    
    SERVICIO_CHOICES = [
        ('manicure', 'Manicure'),
        ('pedicure', 'Pedicure'),
        ('pigmentacion de cejas', 'Pigmentación de cejas'),
        ('depilacion', 'Depilación'),
    ]
    
    PROFESIONAL_CHOICES = [
        ('Camila', 'Camila'),
        ('Lorena', 'Lorena'),
        ('Stefany', 'Stefany'),
        ('Clara', 'Clara'),
        ('Heidy', 'Heidy'),
    ]
    
    # Relaciona la cita con el usuario que inició sesión
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='citas')
    servicio = models.CharField(max_length=100, choices=SERVICIO_CHOICES)
    profesional = models.CharField(max_length=50, choices=PROFESIONAL_CHOICES, default='Camila')
    fecha = models.DateField()
    hora = models.TimeField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    descripcion_no_atendida = models.TextField(blank=True, null=True, help_text="Descripción opcional si la cita no se realizó")

    class Meta:
        # Evitar citas duplicadas: el mismo profesional no puede tener dos citas a la misma hora
        unique_together = ('profesional', 'fecha', 'hora')

    def __str__(self):
        return f"Cita de {self.usuario.username} - {self.servicio} ({self.fecha} {self.hora})"

class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_codes')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=2)

    def __str__(self):
        estado = 'Usado' if self.used else 'Activo'
        return f"Código {self.code} para {self.user.email} ({estado})"

