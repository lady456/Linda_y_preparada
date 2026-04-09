from django.urls import path
from . import views

urlpatterns =[
    path ('', views.inicio, name='inicio'),
    path ('citas', views.citas, name='citas'),
    path ('confirmacion/', views.confirmacion, name='confirmacion'),
    path ('formulario', views.formulario, name='formulario'),
    path ('mis_citas', views.mis_citas, name='mis_citas'),
    path ('recuperar-contrasena', views.password_reset_request, name='password_reset_request'),
    path ('recuperar-contrasena/validar-codigo/', views.password_reset_verify, name='password_reset_verify'),
    path ('recuperar-contrasena/nueva-contrasena/', views.password_reset_confirm, name='password_reset_confirm'),
    path ('verificacion', views.verificacion, name='verificacion'), 
    path ('administrador', views.administrador, name='administrador'),
    path ('crear_administrador', views.crear_administrador, name='crear_administrador'),
    path ('reprogramar_cita/<int:cita_id>/', views.reprogramar_cita, name='reprogramar_cita'),
    path ('cancelar_cita/<int:cita_id>/', views.cancelar_cita, name='cancelar_cita'),
    path ('marcar_atendida/<int:cita_id>/', views.marcar_atendida, name='marcar_atendida'),
    path ('marcar_no_atendida/<int:cita_id>/', views.marcar_no_atendida, name='marcar_no_atendida'),
    path ('api/obtener-horas-disponibles/', views.obtener_horas_disponibles, name='obtener_horas_disponibles'),
]