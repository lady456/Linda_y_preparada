from django.urls import path
from . import views

urlpatterns =[
    path ('', views.inicio, name='inicio'),
    path ('citas', views.citas, name='citas'),
    path ('confirmacion', views.confirmacion, name='confirmacion'),
    path ('login', views.login, name='login'),
    path ('verificacion', views.verificacion, name='verificacion'),
    path ('registro_usu', views.registro_usu, name='registro_usu'),
    
    ]
