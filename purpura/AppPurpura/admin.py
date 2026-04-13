from django.contrib import admin
from .models import Cita, PasswordResetCode

# Register your models here.
admin.site.register(Cita)
admin.site.register(PasswordResetCode)
