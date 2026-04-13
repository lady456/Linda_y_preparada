 MANUAL TÉCNICO - SISTEMA PURPURA
 Sistema de Gestión de Citas para Salón de Belleza

**Versión:** 1.0  
**Fecha:** 13 de abril de 2026  
**Autor:** Valentina Barahona, Leidy Ruiz y Elias Lugo

---

 TABLA DE CONTENIDOS

1. Introducción
2. Objetivos del Sistema
3. Requisitos del Sistema
4. Arquitectura del Software
5. Instalación y Configuración
6. Descripción de Módulos y Funciones
7. Interfaz de Usuario
8. APIs y Servicios Externos
9. Seguridad
10. Pruebas y Depuración
11. Mantenimiento y Actualizaciones
12. Resolución de Problemas
13. Anexos

---

 INTRODUCCIÓN

 ¿Qué es Purpura?

**Purpura** es un sistema web de gestión de citas para salones de belleza, desarrollado con **Django 6.0.2** (Framework Python) y **SQLite3**. Permite a los clientes agendar citas para servicios de belleza y a los administradores gestionar, confirmar, reprogramar y registrar el cumplimiento de las citas.

Propósito

Facilitar la administración eficiente de citas en un salón de belleza, automatizando:
- Registro y autenticación de usuarios
- Agendamiento de servicios
- Validación de horarios disponibles
- Gestión administrativa de citas
- Recuperación de contraseñas mediante códigos seguros

 Público Objetivo

- **Usuarios Clientes:** Personas que desean agendar servicios de belleza
- **Administradores (Profesionales):** Personal del salón encargado de gestionar citas
- **Superusuario:** Administrador general del sistema

 Versión

- **Versión Actual:** 1.0
- **Última Actualización:** 13/04/2026
- **Framework:** Django 6.0.2
- **Base de Datos:** SQLite3
- **Python:** 3.9+

---

 OBJETIVOS DEL SISTEMA

 Objetivo General

Proveer una plataforma web que simplifique la gestión de citas de un salón de belleza, mejorando la experiencia del cliente y optimizando el tiempo de las profesionales.

 Objetivos Específicos

1. **Permitir registro seguro** de nuevos usuarios con validación de email
2. **Facilitar agendamiento** de citas con disponibilidad en tiempo real
3. **Validar conflictos** de horarios para evitar doble booking
4. **Proporcionar panel administrativo** para gestión de citas
5. **Implementar recuperación de contraseña** mediante códigos de validación
6. **Controlar acceso** diferenciado por rol (usuario, admin, superadmin)
7. **Mantener historial** de citas completadas y canceladas

---

 REQUISITOS DEL SISTEMA

 Requisitos de Hardware

| Componente | Mínimo | Recomendado |
|-----------|--------|------------|
| **Procesador** | Intel i3 / AMD Ryzen 3 | Intel i5 / AMD Ryzen 5 |
| **RAM** | 2 GB | 4 GB |
| **Disco Duro** | 500 MB libres | 1 GB libres |
| **Red** | Conexión a Internet | Conexión de banda ancha |

 Requisitos de Software

 Servidor

- **Sistema Operativo:** Windows 10+, Linux (Ubuntu 20.04+), macOS 10.15+
- **Python:** 3.9, 3.10, 3.11, 3.12
- **Django:** 6.0.2
- **Base de Datos:** SQLite3 (incluido con Python)

 Cliente (Navegador)

- **Chrome** 90+
- **Firefox** 88+
- **Safari** 14+
- **Edge** 90+

 Dependencias Python

```
Django==6.0.2
python-decouple==3.8
django-crispy-forms==2.1
Pillow==10.0.0
```

 Variables de Entorno Necesarias

```
DEBUG=True (desarrollo) o False (producción)
SECRET_KEY=tu_clave_secreta_django
ALLOWED_HOSTS=localhost,127.0.0.1
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend (desarrollo)
EMAIL_HOST=smtp.gmail.com (producción)
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_correo@gmail.com
EMAIL_HOST_PASSWORD=tu_contraseña_app
```

---

 ARQUITECTURA DEL SOFTWARE

 Diagrama General de Componentes

```
┌─────────────────────────────────────────────────────────┐
│              SISTEMA PURPURA                             │
├─────────────────────────────────────────────────────────┤
│                  INTERFAZ DE USUARIO (HTML/CSS)          │
│  (Navegador Web: Chrome, Firefox, Safari, Edge)          │
├─────────────────────────────────────────────────────────┤
│               FRAMEWORK DJANGO (Python)                  │
│  ┌──────────────────────────────────────────────────┐   │
│  │  CAPAS DE DJANGO                                │   │
│  ├──────────────────────────────────────────────────┤   │
│  │  • Views (Lógica de negocio)                    │   │
│  │  • Forms (Validación de datos)                  │   │
│  │  • Models (Modelos de datos)                    │   │
│  │  • URLs (Enrutamiento)                          │   │
│  │  • Templates (Presentación)                     │   │
│  └──────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│              BASE DE DATOS SQLite3                       │
│  (Tablas: Auth_User, AppPurpura_Cita, etc.)             │
└─────────────────────────────────────────────────────────┘
```

 Estructura de Directorios

```
purpura/
├── manage.py                          # Gestor de Django
├── db.sqlite3                         # Base de datos
├── MANUAL_TECNICO.md                 # Este documento
│
├── purpura/                           # Configuración del proyecto
│   ├── settings.py                   # Configuración general
│   ├── urls.py                       # URLs principales
│   ├── wsgi.py                       # Servidor WSGI
│   └── asgi.py                       # Servidor ASGI
│
└── AppPurpura/                        # Aplicación principal
    ├── models.py                     # Modelos de datos
    ├── views.py                      # Vistas (lógica)
    ├── forms.py                      # Formularios
    ├── urls.py                       # URLs de la app
    ├── admin.py                      # Panel admin Django
    ├── apps.py                       # Configuración de app
    │
    ├── migrations/                   # Cambios de BD
    │   ├── 0001_initial.py
    │   ├── 0002_cita_delete_registro.py
    │   ├── 0003_cita_estado_cita_profesional...py
    │   ├── 0004_alter_cita_estado...py
    │   ├── 0005_passwordresetcode.py
    │   └── 0006_cita_descripcion_no_atendida...py
    │
    ├── static/                       # Archivos estáticos (CSS, JS, img)
    │   └── pagina/
    │       └── css/
    │           ├── Styles.css
    │           ├── prueba.css
    │           └── img/
    │
    └── templates/                    # Plantillas HTML
        ├── base.html                 # Plantilla base
        ├── paginas/
        │   ├── inicio.html
        │   ├── citas.html
        │   ├── confirmacion.html
        │   ├── login.html
        │   └── reprogramar.html
        │
        ├── sistema/
        │   ├── administrador.html
        │   ├── crear_administrador.html
        │   └── no_atendida.html
        │
        └── usuarios/
            ├── formulario.html
            ├── mis_citas.html
            ├── password_reset_request.html
            ├── password_reset_verify.html
            ├── password_reset_confirm.html
            ├── verificacion.html
            └── style.css
```

 Modelos de Datos

 Modelo: Cita

```python
class Cita(models.Model):
    usuario = ForeignKey(User)              # Usuario que agendó
    servicio = CharField                    # (Manicure, Pedicure, etc.)
    profesional = CharField                 # (Camila, Lorena, Stefany, Clara, Heidy)
    fecha = DateField                       # Fecha de la cita
    hora = TimeField                        # Hora de la cita
    estado = CharField                      # (PENDIENTE, CONFIRMADA, REPROGRAMADA, 
                                           #  CANCELADA, ATENDIDA)
    descripcion_no_atendida = TextField    # Razón si no se atendió
    
    Restricción Única: (profesional, fecha, hora)
```

 Modelo: PasswordResetCode

```python
class PasswordResetCode(models.Model):
    user = ForeignKey(User)                 # Usuario
    code = CharField(6 dígitos)            # Código de verificación
    created_at = DateTimeField             # Fecha de creación
    used = BooleanField                    # ¿Ya se usó?
    Expiración: 2 minutos
```

 Modelo: User (Django Auth)

```python
class User(models.Model):                  # Usuario de Django
    username = CharField                   # Nombre de usuario
    email = EmailField                     # Correo
    password = CharField (hashed)          # Contraseña encriptada
    is_staff = BooleanField               # ¿Es administrador?
    is_superuser = BooleanField           # ¿Es superusuario?
```

---

 INSTALACIÓN Y CONFIGURACIÓN

Paso 1: Preparar el Entorno

 En Windows:

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
venv\Scripts\activate

# Instalar dependencias
pip install Django==6.0.2
pip install python-decouple
pip install django-crispy-forms
pip install Pillow
```

 En Linux/macOS:

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
pip install Django==6.0.2
pip install python-decouple
pip install django-crispy-forms
pip install Pillow
```

Paso 2: Configurar la Base de Datos

```bash
# Crear/aplicar migraciones
python manage.py migrate

# Crear superusuario (administrador)
python manage.py createsuperuser
# Ingresa:
# - Username: admin
# - Email: admin@saloon.com
# - Password: tu_contraseña_segura
```

 Paso 3: Recopilar Archivos Estáticos

```bash
python manage.py collectstatic
```

 Paso 4: Ejecutar el Servidor de Desarrollo

```bash
python manage.py runserver
```

Accede a: http://127.0.0.1:8000

 Paso 5: Configurar Correo Electrónico (Opcional pero Recomendado)

Edita `purpura/settings.py`:

```python
# Para desarrollo (consola)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Para producción (Gmail)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu_correo@gmail.com'
EMAIL_HOST_PASSWORD = 'tu_contraseña_app'  # NO la contraseña real, una del lado de Gmail
DEFAULT_FROM_EMAIL = 'tu_correo@gmail.com'
```

---

 DESCRIPCIÓN DE MÓDULOS Y FUNCIONES

1. Módulo: Models (models.py)

Define la estructura de datos del sistema.

 Función: Cita Model
**Propósito:** Almacenar información de citas  
**Campos:** usuario, servicio, profesional, fecha, hora, estado, descripcion_no_atendida  
**Validaciones:**
- No permite citas duplicadas (mismo profesional, fecha, hora)
- Estados permitidos: PENDIENTE, CONFIRMADA, REPROGRAMADA, CANCELADA, ATENDIDA

 Función: PasswordResetCode Model
**Propósito:** Almacenar códigos temporales de recuperación de contraseña  
**Validaciones:**
- Códigos válidos por 2 minutos
- Se marca como usado después de validarse

 2. Módulo: Views (views.py)

Contiene la lógica de negocio. Funciones principales:

 Función: CustomLoginView
**Propósito:** Manejo de login personalizado  
**Parámetros:** request (HTTP)  
**Retorna:** Redirección a panel admin (si es superuser/staff) o a mis_citas (si es cliente)

 Función: citas(request)
**Propósito:** Mostrar la página de agendamiento de citas  
**Parámetros:** request (HTTP)  
**Retorna:** Template citas.html con formulario

 Función: confirmacion(request)
**Propósito:** Mostrar resumen antes de confirmar cita  
**Parámetros:** request, servicio, fecha, hora (GET)  
**Retorna:** Template confirmacion.html

 Función: formulario(request)
**Propósito:** Página de registro de usuarios  
**Métodos:** GET (mostrar form), POST (procesar registro)  
**Retorna:** Redirect a citas si es exitoso

 Función: mis_citas(request)
**Propósito:** Mostrar todas las citas del usuario logueado  
**Requerimientos:** Usuario debe estar autenticado  
**Retorna:** Template mis_citas.html con listado ordenado

Función: administrador(request)
**Propósito:** Panel administrativo de citas  
**Filtros:** Por profesional, estado  
**Requerimientos:** Usuario debe ser staff o superuser  
**Retorna:** Template administrador.html con estadísticas

 Función: password_reset_request(request)
**Propósito:** Primer paso de recuperación de contraseña  
**Proceso:** Usuario ingresa email → Se envía código  
**Validaciones:** Email debe estar registrado

 Función: password_reset_verify(request)
**Propósito:** Validar código de 6 dígitos  
**Validaciones:** Código no expirado, no usado, válido  
**Duración código:** 2 minutos

 Función: password_reset_confirm(request)
**Propósito:** Cambiar contraseña después de validar código  
**Nota:** Elimina todas las citas previas del usuario

 Función: reprogramar_cita(request, cita_id)
**Propósito:** Cambiar fecha/hora de una cita existente  
**Restricción:** Solo si falta 3+ horas  
**Cambia estado a:** REPROGRAMADA

 Función: cancelar_cita(request, cita_id)
**Propósito:** Cancelar una cita  
**Restricción:** Solo si falta 3+ horas  
**Cambia estado a:** CANCELADA

 Función: marcar_atendida(request, cita_id)
**Propósito:** Registrar que se completó una cita  
**Requerimientos:** Solo superuser  
**Cambia estado a:** ATENDIDA

 Función: marcar_no_atendida(request, cita_id)
**Propósito:** Registrar cita no realizada con descripción  
**Requerimientos:** Solo superuser  
**Cambia estado a:** CANCELADA

 Función: obtener_horas_disponibles(request)
**Propósito:** API JSON que retorna horarios libres  
**Parámetros:** profesional, fecha (GET)  
**Retorna:** JSON con horas disponibles

 3. Módulo: Forms (forms.py)

Valida datos de entrada.

 Form: RegistroUsuarioForm
**Campos:** username, password, password_confirmation, email, verificacion_humano  
**Validaciones:** Email único, contraseñas coinciden, captcha

 Form: CitaForm
**Campos:** servicio, profesional, fecha, hora  
**Validaciones:** Fecha no puede ser pasada, hora debe estar disponible

 Form: ReprogramarCitaForm
**Campos:** servicio, profesional, fecha, hora  
**Validaciones:** No causa conflicto de horarios

 Form: PasswordResetRequestForm
**Campo:** email  
**Validación:** Email debe existir en sistema

 Form: PasswordResetCodeForm
**Campos:** email, code (6 dígitos)  
**Validación:** Código válido, no expirado, no usado

 Form: NoAtendidaForm
**Campo:** descripcion (texto)  
**Uso:** Registrar razón de no asistencia

 4. Módulo: URLs (urls.py)

Define las rutas del sistema.

| Ruta | Vista | Método | No. |
|------|-------|--------|-----|
| `/` | inicio | GET | 1 |
| `/citas` | citas | GET/POST | 2 |
| `/confirmacion/` | confirmacion | GET | 3 |
| `/formulario` | formulario | GET/POST | 4 |
| `/mis_citas` | mis_citas | GET | 5 |
| `/recuperar-contrasena` | password_reset_request | GET/POST | 6 |
| `/recuperar-contrasena/validar-codigo/` | password_reset_verify | GET/POST | 7 |
| `/recuperar-contrasena/nueva-contrasena/` | password_reset_confirm | GET/POST | 8 |
| `/verificacion` | verificacion | GET | 9 |
| `/administrador` | administrador | GET | 10 |
| `/crear_administrador` | crear_administrador | GET/POST | 11 |
| `/reprogramar_cita/<id>/` | reprogramar_cita | GET/POST | 12 |
| `/cancelar_cita/<id>/` | cancelar_cita | GET/POST | 13 |
| `/marcar_atendida/<id>/` | marcar_atendida | POST | 14 |
| `/marcar_no_atendida/<id>/` | marcar_no_atendida | GET/POST | 15 |
| `/api/obtener-horas-disponibles/` | obtener_horas_disponibles | GET (JSON) | 16 |

---

 INTERFAZ DE USUARIO

 Estructura de Navegación

```
Inicio (LOGIN)
├── Sin Autenticación
│   └── Login → Registro
│
├── Usuario Autenticado (Cliente)
│   ├── Inicio
│   ├── Agendar Cita
│   ├── Mis Citas
│   └── Recuperar Contraseña
│
└── Administrador (Staff/Superuser)
    ├── Panel Administrativo
    ├── Crear Nuevo Admin
    ├── Gestionar Citas
    └── Recuperar Contraseña
```

 Pantallas Principales

 1. **Página de Inicio (inicio.html)**
- Bienvenida general al sistema
- Opciones: Login, Registro, Información

 2. **Login (login.html)**
- Campo: Usuario y Contraseña
- Opciones: Recuperar Contraseña, Crear Cuenta
- Redirección automática según rol

 3. **Registro (formulario.html)**
- Campos: Username, Email, Contraseña, Confirmación, Verificación Humano
- Validaciones: Email único, contraseñas coinciden
- Redirección: A citas tras registro exitoso

 4. **Agendar Cita (citas.html)**
- Selecciona: Servicio (dropdown)
- Selecciona: Profesional (dropdown)
- Selector: Fecha (calendar)
- Selector: Hora (dinámicas según disponibilidad)
- Botón: Confirmar → Ir a confirmacion.html

 5. **Confirmación (confirmacion.html)**
- Resumen: Servicio, Profesional, Fecha, Hora
- Botones: Confirmar Cita, Editar

 6. **Mis Citas (mis_citas.html)**
- Tabla con citas ordenadas por (fecha DESC, hora DESC)
- Columnas: Servicio, Profesional, Fecha, Hora, Estado
- Botones por cita: Ver, Reprogramar (si faltan 3+ horas), Cancelar (si faltan 3+ horas)

 7. **Panel Administrativo (administrador.html)**
- Secciones por Estado: Pendientes, Reprogramadas, Canceladas, Atendidas
- Filtro opcional: Por Profesional
- Tabla de citas con acciones:
  - Si staff: Ver solo sus citas
  - Si superuser: Ver todas, marcar Atendida/No Atendida, crear nuevos admins

 8. **Recuperar Contraseña (3 pasos)**
   - **Step 1 (password_reset_request.html):** Email → Envía código
   - **Step 2 (password_reset_verify.html):** Valida código (2 min)
   - **Step 3 (password_reset_confirm.html):** Nueva contraseña
 
  Elementos Visuales

- **Colores Principales:** Relacionados a salón de belleza (purpura/rosa)
- **Tipo de Letra:** Sans-serif legible (Helvetica, Arial, Roboto)
- **Diseño:** Responsive (funciona en móvil, tablet, desktop)
- **Iconos:** Checklist, calendario, reloj, usuario, logout
- **Mensajes:** Success, Error, Warning en verde, rojo, naranja

---

 APIs Y SERVICIOS EXTERNOS

 API Interna: obtener_horas_disponibles

**Endpoint:** `/api/obtener-horas-disponibles/`  
**Método:** GET  
**Parámetros Requeridos:**
- `profesional` (str): Nombre de la profesional
- `fecha` (str): Fecha en formato YYYY-MM-DD

**Respuesta Exitosa (200):**
```json
{
    "horas_disponibles": [
        "09:00",
        "09:30",
        "10:00",
        "10:30",
        "11:00"
    ],
    "profesional": "Camila",
    "fecha": "2026-04-15"
}
```

**Respuesta Error (400):**
```json
{
    "error": "Parámetros faltantes"
}
```

**Uso desde Frontend (JavaScript):**
```javascript
fetch('/api/obtener-horas-disponibles/?profesional=Camila&fecha=2026-04-15')
    .then(response => response.json())
    .then(data => {
        console.log(data.horas_disponibles);
    });
```

 Servicio Externo: Correo Electrónico

**Uso:** Recuperación de contraseña  
**Servidor:** SMTP de Gmail (producción) o consola (desarrollo)  
**Configuración en settings.py:**

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'desarrollo.purpura@gmail.com'
EMAIL_HOST_PASSWORD = 'tu_app_password'
```

**Plantilla de Correo:**
```
Asunto: Código de recuperación de contraseña

Hola [username],

Usa este código para restablecer tu contraseña: [código 6 dígitos]
El código es válido por 2 minutos.

Si no lo usas, vuelve a solicitar uno nuevo.

Equipo Purpura
```

---

 SEGURIDAD

 1. Autenticación

- **Sistema:** Contraseñas hasheadas con PBKDF2 (Django default)
- **Sesiones:** Cookies seguras lado servidor
- **CSRF Protection:** Tokens CSRF en todos los formularios
- **Logout:** Destruye sesión completamente

 2. Autorización (Permisos)

```python
# Solo usuarios autenticados
@login_required
def mis_citas(request): ...

# Solo staff/superuser
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def administrador(request): ...

# Solo superuser
@user_passes_test(lambda u: u.is_superuser)
def crear_administrador(request): ...
```

 3. Validación de Datos

- **Formularios Django:** Validación server-side
- **Modelos:** Restricción unique_together en Cita
- **Sanitización:** Django templating auto-escapa XSS

 4. Contraseñas

- **Requisitos:**
  - Mínimo 8 caracteres
  - No puede ser solo números
  - No puede contener username
  - Django valida automáticamente

- **Recuperación Segura:**
  - Código temporal 6 dígitos
  - Expira en 2 minutos
  - Se marca como usado tras validarse
  - No se resuelve por email

 5. Base de Datos

- **Ubicación:** `/path/to/db.sqlite3`
- **Permisos:** Restringir acceso a usuarios del sistema
- **Copias de Seguridad:** Realizar diario

6. HTTPS (Producción)

- **Requerimiento:** Django debe servirse con HTTPS
- **Cookies:** Configurar `SESSION_COOKIE_SECURE = True`
- **Headers:** `SECURE_SSL_REDIRECT = True`

 7. Secreto de Django

```python
# NO COMPARTIR BAJO NINGUNA CIRCUNSTANCIA
SECRET_KEY = 'django-insecure-o23u)5x@l4hp=h8g3=dj8s%jl)*=d@z-@r^^^#wtt9#!i+8-fb'

# En producción usar variable de entorno:
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
```

 8. Inyección SQL

- **Protección:** Django ORM previene automáticamente
- **Uso Correcto:**
  ```python
  # ✅ Seguro
  User.objects.filter(email=email)
  
  # ❌ NUNCA hacer esto
  # raw SQL: "SELECT * FROM users WHERE email = '" + email + "'"
  ```

---

 PRUEBAS Y DEPURACIÓN

 Herramientas Utilizadas

1. **Django Debug Toolbar** (Opcional)
   ```bash
   pip install django-debug-toolbar
   ```

2. **Django Test Framework**
   ```bash
   python manage.py test AppPurpura
   ```

3. **Pytest** (Opcional)
   ```bash
   pip install pytest pytest-django
   pytest
   ```

 Métodos de Prueba Realizadas

 1. Pruebas Unitarias

**Archivo sugerido:** `AppPurpura/tests.py`

```python
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Cita
from datetime import date, time

class CitaTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='test123456'
        )
    
    def test_crear_cita(self):
        cita = Cita.objects.create(
            usuario=self.user,
            servicio='manicure',
            profesional='Camila',
            fecha=date.today(),
            hora=time(10, 0),
            estado='PENDIENTE'
        )
        self.assertEqual(cita.usuario.username, 'testuser')
    
    def test_restriccion_unique_together(self):
        # No permite dos citas misma profesional, fecha, hora
        cita1 = Cita.objects.create(
            usuario=self.user,
            servicio='manicure',
            profesional='Camila',
            fecha=date.today(),
            hora=time(10, 0)
        )
        with self.assertRaises(Exception):
            cita2 = Cita.objects.create(
                usuario=self.user,
                servicio='pedicure',
                profesional='Camila',
                fecha=date.today(),
                hora=time(10, 0)
            )
```

 2. Pruebas de Integración

**Rutas a probar:**

| Ruta | Usuario | Esperado |
|------|---------|----------|
| `/formulario` (POST) | Anónimo | Registro exitoso |
| `/login` (POST) | Anónimo | Login exitoso |
| `/citas` | Autenticado | Mostrar formulario |
| `/mis_citas` | Autenticado | Mostrar citas del usuario |
| `/administrador` | No staff | Error 403 |
| `/administrador` | Staff | Mostrar panel |

 3. Pruebas Manuales (Testing Exploratorio)

```
CASO 1: Registro de usuario
1. Ir a /formulario
2. Llenar formulario con datos válidos
3. Enviar
4. Verificar: Usuario creado y sesión iniciada

CASO 2: Agendar cita
1. Iniciar sesión
2. Ir a /citas
3. Seleccionar: Servicio, Profesional, Fecha, Hora
4. Confirmar
5. Verificar: Cita en /mis_citas

CASO 3: Recuperar contraseña
1. En login, click "Recuperar contraseña"
2. Ingresar email
3. Verificar: Email recibido
4. Ingresar código
5. Nueva contraseña
6. Verificar: Puedo iniciar sesión

CASO 4: Evitar doble booking
1. Como Admin1: Agendar cita Camila 10:00
2. Como Admin2: Intentar agendar Camila 10:00
3. Verificar: Sistema rechaza (error unique_together)
```

 Procedimiento de Depuración

 Error Común 1: `django.core.exceptions.ImproperlyConfigured`

**Causa:** INSTALLED_APPS no tiene 'AppPurpura'

**Solución:**
```python
# settings.py
INSTALLED_APPS = [
    ...
    'AppPurpura',  # ← Agregar esto
]
```

 Error Común 2: `Cita matching query does not exist`

**Causa:** Intentar acceder cita de otro usuario sin ser superuser

**Solución:**
```python
# Usar _get_cita_for_action() que ya valida permisos
cita = _get_cita_for_action(request, cita_id)
```

 Error Común 3: No se envía email

**Causa:** EMAIL_BACKEND mal configurado

**Solución:**
```bash
# Desarrollo: Mostrar en consola
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Producción: Usar SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
```

 Activar Modo Debug

```python
# settings.py
DEBUG = True  # ← Mostrar errores detallados

# En producción: DEBUG = False y configurar ALLOWED_HOSTS
```

---
 MANTENIMIENTO Y ACTUALIZACIONES

 Estrategia de Respaldo

 Copias de Seguridad Diarias

```bash
# Script Windows: backup.bat
@echo off
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
copy c:\LYP\purpura\db.sqlite3 c:\LYP\backups\db_%mydate%.sqlite3
echo Backup realizado: %mydate%

# Script Linux: backup.sh
#!/bin/bash
DATE=$(date +%Y-%m-%d)
cp /path/to/purpura/db.sqlite3 /path/to/backups/db_$DATE.sqlite3
echo "Backup realizado: $DATE"

# Ejecutar diariamente con cron
# Editar: crontab -e
# Agregar: 0 2 * * * /path/to/backup.sh
```

 Almacenamiento

- **Local:** Mínimo 30 días histórico
- **Cloud:** AWS S3, Google Drive, Azure (opcional)
- **Compresión:** ZIP para ahorrar espacio

 Actualización de Dependencias

 Paso 1: Verificar versiones actuales

```bash
pip show Django
pip list
```

 Paso 2: Crear ambiente de prueba

```bash
python -m venv venv_test
venv_test\Scripts\activate
pip install -r requirements.txt
```

 Paso 3: Actualizar Django

```bash
pip install --upgrade Django

# Ejecutar migraciones
python manage.py migrate
```

 Paso 4: Pruebas completas

```bash
python manage.py test AppPurpura
python manage.py runserver
# Probar manualmente todas las funciones críticas
```

 Paso 5: Actualizar producción

```bash
# En servidor de producción
python manage.py migrate
systemctl restart gunicorn  # Si usas Gunicorn
```

 Parches de Seguridad

**Verificar vulnerabilidades:**

```bash
pip install safety
safety check
```

**Aplicar parches urgentes:**

```bash
pip install --upgrade Django
pip install --upgrade Pillow
# etc.
```

 Registros (Logs)

**Ubicación sugerida:** `logs/django.log`

**Configuración en settings.py:**

```python
LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'ERROR',
    },
}
```

 Monitoreo de Rendimiento

**Métricas a monitorear:**

- Tiempo respuesta promedio (< 2 segundos)
- Uso de base de datos (queries por request)
- Espacio disco (alertar al 80%)
- Errores 500 (Zero tolerance)

---

 RESOLUCIÓN DE PROBLEMAS

 Error: `python: can't open file 'C:\\LYP\\purpura\\venv'`

**Causa:** Entorno virtual no existe

**Solución:**
```bash
cd C:\LYP\purpura
python -m venv venv
```

 Error: `No module named 'django'`

**Causa:** Django no instalado en el entorno activo

**Solución:**
```bash
pip install Django==6.0.2
```

 Error: `CSRF verification failed`

**Causa:** Token CSRF faltante en formulario

**Solución:**
```html
<!-- En todo formulario POST -->
<form method="POST">
    {% csrf_token %}
    <!-- campos del formulario -->
</form>
```

 Error: `OperationalError: no such table: AppPurpura_cita`

**Causa:** Migración no aplicada

**Solución:**
```bash
python manage.py migrate
```

 Error: `Cita matching query does not exist`

**Causa:** ID de cita inválido o permisos insuficientes

**Solución:**
```python
# Usar get_object_or_404 para manejar gracefully
from django.shortcuts import get_object_or_404
cita = get_object_or_404(Cita, id=cita_id, usuario=request.user)
```

 Email no se envía

**Checklist:**
- ✓ EMAIL_BACKEND correctamente configurado
- ✓ EMAIL_HOST_USER es correo realista
- ✓ EMAIL_HOST_PASSWORD es token (no contraseña)
- ✓ EMAIL_PORT = 587 para TLS
- ✓ Conexión a internet disponible

**Prueba:**
```bash
python manage.py shell
from django.core.mail import send_mail
send_mail('Test', 'Mensaje de prueba', 'from@example.com', ['to@example.com'])
```

 Base de datos corrupta

**Recuperación completa:**

```bash
# Hacer backup
copy db.sqlite3 db.sqlite3.bak

# Eliminar
del db.sqlite3

# Recrear
python manage.py migrate

# Restaurar data (si hay backup limpio)
```

 Servidor lento

**Optimización:**

```python
# settings.py
# 1. Usar select_related() para FK
citas = Cita.objects.select_related('usuario').all()

# 2. Usar only() para campos específicos
usuarios = User.objects.only('username', 'email')

# 3. Usar cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# 4. Paginar resultados
from django.core.paginator import Paginator
paginator = Paginator(citas, 20)  # 20 por página
```

 Contacto de Soporte Técnico

**Para problemas no resueltos:**
- Email: lvbp2008@gmail.com
- Teléfono: 3508668592
- Repositorio: github.com/purpura/sistema

---

 ANEXOS

 A. Códigos Fuente Relevantes

 A.1. Validación de Horarios Disponibles

```python
def obtener_horas_disponibles(request):
    profesional = request.GET.get('profesional')
    fecha = request.GET.get('fecha')
    
    if not profesional or not fecha:
        return JsonResponse({'error': 'Parámetros faltantes'}, status=400)
    
    # Horas disponibles: 9 AM a 6 PM, cada 30 min
    horas = ['09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00',
             '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30',
             '16:00', '16:30', '17:00', '17:30', '18:00']
    
    # Citas ocupadas ese día
    ocupadas = Cita.objects.filter(
        profesional=profesional,
        fecha=fecha,
        estado__in=['PENDIENTE', 'CONFIRMADA', 'REPROGRAMADA']
    ).values_list('hora', flat=True)
    
    horas_disponibles = [h for h in horas if h not in ocupadas]
    
    return JsonResponse({
        'horas_disponibles': horas_disponibles,
        'profesional': profesional,
        'fecha': fecha
    })
```

 A.2. Helper: Puede Modificar Cita

```python
def _can_modify_cita(cita):
    """Verifica si quedan 3+ horas antes de la cita"""
    from datetime import datetime, timedelta
    cita_datetime = datetime.combine(cita.fecha, cita.hora)
    return cita_datetime - datetime.now() >= timedelta(hours=3)
```

 A.3. Envío de Correo de Recuperación

```python
def _send_reset_code(user):
    """Genera, almacena y envía código de reseteo"""
    code = f"{random.randint(100000, 999999)}"
    PasswordResetCode.objects.create(user=user, code=code)
    
    subject = 'Código de recuperación de contraseña'
    message = (
        f'Hola {user.username},\n\n'
        f'Usa este código para restablecer tu contraseña: {code}\n'
        'El código es válido por 2 minutos.\n\n'
        'Si no usas el código, vuelve a solicitar uno nuevo.\n'
    )
    send_mail(subject, message, None, [user.email])
```

 B. Configuración Recomendada para Producción

```python
# settings.py - Producción

DEBUG = False

ALLOWED_HOSTS = ['tu-dominio.com', 'www.tu-dominio.com']

# Seguridad
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
}

# Base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # O MySQL
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')

# Logs
LOGGING = {...}

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

 C. Archivo requirements.txt

```
Django==6.0.2
python-decouple==3.8
django-crispy-forms==2.1
Pillow==10.0.0
gunicorn==21.2.0
psycopg2-binary==2.9.3
python-dotenv==1.0.0
```

 D. Glosario de Términos

| Término | Significado |
|---------|------------|
| **Cita** | Reserva de un servicio en una fecha/hora específica |
| **Profesional** | Estilista o esteticien del salón |
| **Estado** | Situación actual de una cita (PENDIENTE, CONFIRMADA, etc.) |
| **Staff** | Administrador con permisos limitados (su profesional) |
| **Superuser** | Administrador con todos los permisos |
| **CSRF** | Cross-Site Request Forgery (prevención de ataques) |
| **ORM** | Object-Relational Mapping (abstracción de base de datos) |
| **Migration** | Cambio de estructura en la base de datos |
| **Middleware** | Componente que procesa requests/responses |
| **Serialización** | Convertir objeto a JSON |

 E. Referencias Externas

- **Django Official:** https://docs.djangoproject.com/
- **Django Best Practices:** https://docs.djangoproject.com/en/stable/intro/
- **Python.org:** https://www.python.org/
- **SQLite Documentation:** https://www.sqlite.org/docs.html

 F. Preguntas Frecuentes (FAQ)

**P: ¿Puedo cambiar la base de datos de SQLite a PostgreSQL?**  
R: Sí, cambiar `DATABASES` en settings.py e instalar `psycopg2-binary`. Luego `python manage.py migrate`.

**P: ¿Puedo agregar más servicios o profesionales?**  
R: Sí, actualizar `SERVICIO_CHOICES` y `PROFESIONAL_CHOICES` en models.py.

**P: ¿Cómo agrego un nuevo campo a Cita?**  
R: Editar models.py, crear migration (`makemigrations`), aplicar (`migrate`).

**P: ¿Puedo usar este sistema en producción?**  
R: Sí, pero seguir la sección de configuración para producción y cambiar `DEBUG = False`.

---
 
 INFORMACIÓN DEL DOCUMENTO

**Versión
** 1.0  
**Fecha Última Actualización:** 13 de abril de 2026  
**Próxima Revisión Recomendada:** 13 de octubre de 2026  
**Responsable de Actualización:** Equipo de Desarrollo  
**Clasificación:** Técnico - Acceso Interno

---

**Fin del Manual Técnico**

Preguntas o sugerencias: eliaslugo315@gmail.com
