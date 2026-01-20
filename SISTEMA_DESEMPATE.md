# Sistema de Desempate de Postulantes

## Resumen

Se ha implementado un **sistema completo de desempate** para el Sistema de Asignación de Cupos (SAC) que permite resolver automáticamente casos donde dos o más postulantes tienen la misma nota en el mismo segmento poblacional.

## Características

### ✅ Criterios Automáticos Predefinidos

El administrador puede elegir entre 5 criterios de desempate automáticos:

1. **Alfabético por Apellido (A-Z)** - Criterio por defecto
2. **Alfabético por Nombre (A-Z)**
3. **Mayor Edad** - Favorece a los más mayores
4. **Menor Edad** - Favorece a los más jóvenes
5. **Fecha de Inscripción** - Orden de inscripción (FIFO)

### ✅ Cambios Manuales

El administrador puede:
- Cambiar manualmente el ordenamiento completo de postulantes en un segmento
- Agregar cambios manuales individuales
- Remover cambios específicos
- Resetear todos los cambios manuales de un segmento

### ✅ Aplicación Automática

El desempate se aplica automáticamente durante la asignación de cupos:
- Se agrupa a postulantes por nota dentro de cada segmento
- Se aplica el criterio de desempate a grupos con múltiples postulantes
- Los cambios manuales tienen prioridad sobre los automáticos

## Componentes Implementados

### 1. Domain Layer

**`domain/criterio_desempate.py`**
- Clase `CriterioDesempate`: Gestiona desempate para un segmento
- Enum `TipoDesempate`: Define tipos de criterios

### 2. Service Layer

**`services/desempate_service.py`**
- Clase `DesempateService`: Servicio principal para gestionar desempates
- Persistencia en JSON
- Obtención de opciones disponibles

### 3. API REST

**`api/desempate_api.py`**
- Endpoints para CRUD de criterios de desempate
- Endpoints para gestión de cambios manuales
- Blueprint registrado en la aplicación Flask

### 4. UI

**`iu/desempates/form_desempates.py`**
- Clase base para UI de desempates

**`templates/desempates/gestionar_desempates.html`**
- Interfaz web completa con dos pestañas:
  - **Criterios Automáticos**: Cambiar criterio por segmento
  - **Cambios Manuales**: Gestión de ordenamientos manuales

### 5. Integración con Asignación

**`patterns/strategy/segmento_asignacion_strategy.py`** (actualizado)
- Método `_aplicar_desempate()` para aplicar desempate automático
- Inyección de servicio de desempate

**`services/asignador_cupos.py`** (actualizado)
- Integración de `DesempateService`
- Inyección en todas las estrategias

### 6. Domain

**`domain/estudiante.py`** (actualizado)
- Campos `fecha_nacimiento` y `fecha_inscripcion` para criterios de edad

## Cómo Usar

### Interfaz Web

1. **Acceso**: `/desempates/gestionar` (requiere autenticación)

2. **Pestaña Criterios Automáticos**:
   - Ver criterio actual para cada segmento
   - Cambiar a otro criterio desde el selector
   - Leer descripción de cada opción

3. **Pestaña Cambios Manuales**:
   - Seleccionar un segmento
   - Ver cambios manuales actuales
   - Agregar nuevo cambio (postulante_id + posición)
   - Remover cambios individuales
   - Resetear todos los cambios del segmento

### API REST

#### Obtener opciones disponibles
```bash
GET /api/desempate/opciones
```

#### Obtener todos los criterios
```bash
GET /api/desempate/criterios
```

#### Obtener criterio de un segmento
```bash
GET /api/desempate/criterio/{segmento_nombre}
```

#### Cambiar criterio automático
```bash
PUT /api/desempate/criterio/{segmento_nombre}
Content-Type: application/json

{
    "tipo_desempate": "mayor_edad"
}
```

#### Establecer ordenamiento manual completo
```bash
POST /api/desempate/ordenamiento-manual/{segmento_nombre}
Content-Type: application/json

{
    "lista_ids": ["P001", "P003", "P002"]
}
```

#### Agregar cambio manual individual
```bash
POST /api/desempate/cambio-manual/{segmento_nombre}
Content-Type: application/json

{
    "postulante_id": "P001",
    "posicion": 0
}
```

#### Remover cambio manual
```bash
DELETE /api/desempate/cambio-manual/{segmento_nombre}/{postulante_id}
```

#### Resetear cambios manuales
```bash
POST /api/desempate/resetear/{segmento_nombre}
```

### Uso Programático

```python
from services.desempate_service import DesempateService
from domain.criterio_desempate import TipoDesempate

# Crear servicio
servicio = DesempateService()

# Cambiar criterio
servicio.establecer_criterio_automatico("Población General", TipoDesempate.MAYOR_EDAD)

# Aplicar desempate
estudiantes_ordenados = servicio.aplicar_desempate(
    "Población General",
    estudiantes_con_misma_nota
)

# Cambio manual
servicio.agregar_cambio_manual("Población General", "P123", 0)
```

## Flujo de Ejecución

```
1. Usuario carga postulantes
2. Usuario ejecuta asignación
3. AsignadorCupos inicializa con DesempateService
4. Para cada segmento:
   a. Se filtran postulantes elegibles
   b. Se ordenan por nota (descendente)
   c. Se aplica _aplicar_desempate():
      - Agrupa por nota
      - Para cada grupo con >1 postulante:
        - Consulta DesempateService
        - Si hay cambios manuales → aplica primero
        - Si no → aplica criterio automático
   d. Se asignan cupos en orden
```

## Persistencia

Los criterios se guardan automáticamente en `data/criterios_desempate.json`:

```json
{
    "Segmento": {
        "segmento_nombre": "Población General",
        "tipo_desempate": "alfabetico_apellido",
        "ordenamiento_manual": {
            "P123": 0,
            "P456": 2
        },
        "fecha_actualizacion": "2026-01-19T..."
    }
}
```

## Pruebas

Se incluye un archivo de pruebas completo en `tests/test_desempate.py`:

```bash
cd "ruta/del/proyecto"
python tests/test_desempate.py
```

**Pruebas incluidas:**
- Desempate alfabético
- Desempate por edad
- Desempate por inscripción
- Desempate manual
- Servicio completo
- Persistencia
- Opciones disponibles

## Consideraciones de Diseño

### Inyección de Dependencias
- El servicio se inyecta en las estrategias
- Facilita testing y cambio de comportamiento

### Prioridad Manual > Automática
- Cambios manuales tienen preferencia
- Permite control administrativo cuando sea necesario

### Extensibilidad
- Fácil agregar nuevos criterios extendiendo `TipoDesempate`
- Lógica centralizada en `DesempateService`

### Atomicidad
- Cambios se guardan inmediatamente
- Recuperación ante errores

## Campos Requeridos

Para que todos los criterios funcionen correctamente, los estudiantes deben incluir:

- `fecha_nacimiento`: `datetime` (para criterios de edad)
- `fecha_inscripcion`: `datetime` (para criterio de inscripción)

Estos campos se cargan desde el CSV de postulantes si están disponibles.

## Seguridad

- Todos los endpoints requieren autenticación
- Validación de datos de entrada
- Manejo seguro de excepciones

## Próximas Mejoras Sugeridas

1. 📊 Vista previa de resultados antes de aplicar desempate
2. 📝 Auditoría de cambios (quién, qué, cuándo)
3. 🔄 Desempate por múltiples criterios
4. 📥 Importación/exportación de configuraciones
5. 📋 Historial de cambios
6. 🎯 Criterios personalizados por usuario

## Contacto / Soporte

Para preguntas o problemas con el sistema de desempate, consultar la documentación en `DESEMPATE_DOCUMENTACION.md`.
