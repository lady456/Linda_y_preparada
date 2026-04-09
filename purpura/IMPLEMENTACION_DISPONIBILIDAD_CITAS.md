# 📅 Sistema de Disponibilidad de Citas - Implementación Completa

## ✅ Cambios Realizados

### 1. **Modelo de Base de Datos** (`models.py`)
- ✨ **Restricción UNIQUE**: Agregada restricción `unique_together` en la combinación `(profesional, fecha, hora)` para evitar citas duplicadas
- Esta restricción garantiza que un profesional no pueda tener dos citas a la misma hora

```python
class Meta:
    unique_together = ('profesional', 'fecha', 'hora')
```

---

### 2. **Formulario de Citas Mejorado** (`forms.py`)

#### **CitaForm**
- ✅ Método `clean()` que valida:
  - No permite agendar si ya existe una cita para ese profesional, fecha y hora
  - Solo considera citas activas (PENDIENTE, CONFIRMADA, REPROGRAMADA)
  - Las citas CANCELADAS no bloquean disponibilidad
  
- 🔧 Método estático `get_horas_disponibles()`:
  - Retorna lista de horas libres para un profesional en una fecha específica
  - Se usa en el endpoint AJAX

#### **ReprogramarCitaForm**
- ✅ Validación mejorada que excluye la cita actual al verificar conflictos
- Permite reprogramar a una franja disponible sin conflictos

---

### 3. **Backend API** (`views.py`)

#### **Nueva vista AJAX**
```python
@login_required
def obtener_horas_disponibles(request):
    """Obtiene horas disponibles para un profesional en una fecha específica"""
    # Retorna JSON con lista de horas libres
```

**Endpoint**: `/AppPurpura/api/obtener-horas-disponibles/`

**Parámetros GET**:
- `profesional`: Nombre del profesional
- `fecha`: Fecha en formato YYYY-MM-DD

**Respuesta JSON**:
```json
{
  "horas": ["07:00", "08:00", "10:00", "11:00"],
  "profesional": "Camila",
  "fecha": "2026-04-15"
}
```

---

### 4. **Frontend Dinámico** (`citas.html`)

#### **Características**
- 🔄 **JavaScript dinámico** que carga horas disponibles en tiempo real
- Cuando el usuario selecciona profesional Y fecha:
  1. Se envía petición AJAX al servidor
  2. El servidor consulta citas existentes
  3. Se devuelven solo las horas libres
  4. El select de horas se actualiza dinámicamente

- 🎨 **Mejoras visuales**:
  - Indicador de carga ("Cargando horas disponibles...")
  - Mejor estructura de formulario con grupos
  - Mensajes de error mejorados
  - Estilos actualizados

#### **Flujo de Usuario**
1. Usuario selecciona **servicio**
2. Usuario selecciona **profesional**
3. Usuario selecciona **fecha**
4. AJAX carga dinámicamente las **horas disponibles**
5. Usuario selecciona una **hora** de las disponibles
6. Envía el formulario

---

### 5. **Rutas** (`urls.py`)
```python
path('api/obtener-horas-disponibles/', views.obtener_horas_disponibles, name='obtener_horas_disponibles'),
```

---

### 6. **Base de Datos** (Migración)
- ✅ Migración `0004_alter_cita_estado_alter_cita_unique_together.py` creada y aplicada
- La BD está lista con la restricción UNIQUE implementada

---

## 🔍 Lógica de Disponibilidad

### **Al Agendar Una Cita**
```
- Catherine quiere agendar con Camila, 15 de Abril, 10:00
- Sistema verifica si existe: 
  Cita WHERE profesional='Camila' AND fecha='2026-04-15' AND hora='10:00'
- Si existe cita activa (no cancelada) → ERROR: "No disponible"
- Si no existe → Se agrega la cita al usuario Catherine
```

### **Al Cancelar/Reprogramar**
- Cita se marca como CANCELADA o REPROGRAMADA
- **Importante**: Si se cancela, la franja vuelve disponible
- Si se reprograma a otra franja, la anterior queda libre

### **Validación en Tiempo Real**
- Horas ocupadas se excluyen del select dinámico
- Usuario solo ve opciones válidas
- Si intenta enviar directamente, el servidor valida (double-check)

---

## 📱 Ejemplo de Uso

### **Escenario 1: Primera cita**
1. Catherine accede a `/citas`
2. Selecciona:
   - Servicio: Manicure
   - Profesional: Camila
   - Fecha: 15/04/2026
3. Sistema consulta AJAX → Horas disponibles: [07:00, 08:00, 10:00, 13:00, 14:00...]
4. Catherine selecciona 10:00
5. Confirma → Cita creada para Catherine

### **Escenario 2: Segundo usuario intenta agendar misma franja**
1. David intenta agendar:
   - Profesional: Camila
   - Fecha: 15/04/2026
2. Sistema consulta AJAX → Horas disponibles: [07:00, 08:00, 13:00, 14:00...] (10:00 FALTA)
3. David no puede ver 10:00 como opción
4. Si intenta enviar directamente código, validación del formulario rechaza

### **Escenario 3: Catherine cancela su cita**
1. Catherine ve la cita en "Mis Citas"
2. Cancela la cita
3. Estado cambia a CANCELADA
4. Franja 10:00 de Camila el 15/04 vuelve disponible
5. David ahora puede agendar a las 10:00

---

## 🛠️ Testing

### **Crear usuarios de prueba**
```bash
# Crear superuser
python manage.py createsuperuser

# O desde shell Django
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.create_user('catherine', 'catherine@test.com', 'pass123')
>>> User.objects.create_user('david', 'david@test.com', 'pass123')
```

### **Probar el sistema**
1. Login como Catherine
2. Ir a `/citas` y agendar una cita
3. Ver en BD que se guardó con el usuario
4. Logout y login como David
5. Intentar agendar misma franja → Debe mostrar error
6. Agendar diferente franja → Debe funcionar
7. Catherine cancela su cita
8. David puede ahora agendar la franja de Catherine (disponible)

---

## 🔐 Seguridad

- ✅ Validación en cliente (JavaScript)
- ✅ Validación en servidor (formulario)
- ✅ Validación en BD (UNIQUE constraint)
- ✅ Solo usuarios autenticados pueden agendar (`@login_required`)
- ✅ Solo pueden ver sus propias citas (excepción: admin ve todas)

---

## 📊 Impacto en Administrador

En la vista de administrador se ven:
- **Citas Pendientes**: Todas las citas nuevas agendadas
- **Citas Reprogramadas**: Las que usuarios han modificado
- **Citas Canceladas**: Las que usuarios han cancelado

Cada cita muestra:
- Usuario que la agendó
- Servicio
- Profesional
- Fecha y hora (sin conflictos)
- Estado actual

---

## 📝 Notas Importantes

1. **Restricción de mes actual**: Las citas solo pueden agendarse en el mes vigente
2. **Horario**: De 7:00 a 17:00 (puede modificarse en `CitaForm.HORA_CHOICES`)
3. **Cancelación**: Requiere 3+ horas de anticipación
4. **Estados**: PENDIENTE, CONFIRMADA, REPROGRAMADA, CANCELADA

---

## 🚀 Próximas Mejoras Opcionales

- [ ] Notifications por email al agendar/cancelar
- [ ] Confirmación de cita por SMS
- [ ] Timeline visual de disponibilidad
- [ ] Estadísticas admin (horas pico, profesional más solicitado)
- [ ] Bloqueo de franjas especiales (almuerzo, descanso)
- [ ] Integración con calendario (Google Calendar)

---

**Estado**: ✅ Implementado y listo para usar
**Fecha**: 9 de Abril de 2026
