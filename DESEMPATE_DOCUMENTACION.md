# Sistema de Desempate de Postulantes - Documentación

## Descripción General

El sistema de desempate permite resolver automáticamente los casos donde dos o más postulantes tienen la misma nota en el mismo segmento poblacional. Ofrece opciones automáticas predefinidas y la posibilidad de hacer cambios manuales por parte del administrador.

## Características Principales

### 1. Criterios de Desempate Automáticos

El sistema ofrece cinco criterios automáticos predefinidos:

- **Alfabético por Apellido (A-Z)**: Ordena a los estudiantes de forma alfabética por apellido. Es el criterio por defecto.
- **Alfabético por Nombre (A-Z)**: Ordena a los estudiantes de forma alfabética por nombre.
- **Mayor Edad**: Favorece a los estudiantes más mayores (más antiguos en edad).
- **Menor Edad**: Favorece a los estudiantes más jóvenes.
- **Fecha de Inscripción**: Ordena por orden de inscripción (quién se inscribió primero).

### 2. Criterios Manuales

El administrador puede realizar cambios manuales en el ordenamiento de postulantes cuando sea necesario.

## Estructura de Clases

### `CriterioDesempate` (domain/criterio_desempate.py)

Representa un criterio de desempate para un segmento específico.

**Atributos:**
- `segmento_nombre`: Nombre del segmento
- `tipo_desempate`: TipoDesempate enum indicando el criterio actual
- `ordenamiento_manual`: Dict con cambios manuales {postulante_id -> posición}
- `fecha_actualizacion`: Timestamp del último cambio

**Métodos principales:**
- `aplicar_desempate(estudiantes_empatados)`: Aplica el desempate a un grupo de estudiantes
- `establecer_ordenamiento_manual(lista_postulante_ids)`: Establece orden manual completo
- `agregar_cambio_manual(postulante_id, posicion)`: Agrega un cambio manual individual
- `cambiar_criterio(nuevo_tipo_desempate)`: Cambia el criterio automático
- `to_dict()` / `from_dict()`: Serialización para persistencia

### `DesempateService` (services/desempate_service.py)

Servicio que gestiona todos los criterios de desempate del sistema.

**Métodos principales:**
- `obtener_criterio(segmento_nombre)`: Obtiene criterio para un segmento
- `obtener_todos_criterios()`: Retorna todos los criterios
- `establecer_criterio_automatico(segmento, tipo)`: Cambia criterio automático
- `establecer_ordenamiento_manual(segmento, lista_ids)`: Establece orden manual
- `aplicar_desempate(segmento, estudiantes)`: Aplica desempate a un grupo
- `obtener_opciones_desempate()`: Retorna lista de opciones disponibles

## Integración con el Sistema de Asignación

### SegmentoAsignacionStrategy

La clase estrategia base ahora incluye:

```python
def _aplicar_desempate(self, estudiantes):
    """Aplica desempate a estudiantes con igual nota"""
    # Agrupa por nota y aplica desempate a cada grupo
```

### AsignadorCupos

Se ha actualizado para inyectar el servicio de desempate:

```python
asignador = AsignadorCupos(
    estudiantes, 
    ofertas,
    desempate_service=DesempateService()
)
```

## API REST

### Endpoints de Desempate

#### GET `/api/desempate/opciones`
Obtiene las opciones disponibles de desempate.

**Respuesta:**
```json
{
    "success": true,
    "opciones": [
        {
            "valor": "alfabetico_apellido",
            "etiqueta": "Alfabético por Apellido (A-Z)",
            "descripcion": "Ordena de forma alfabética por apellido"
        },
        ...
    ]
}
```

#### GET `/api/desempate/criterios`
Obtiene todos los criterios de desempate.

**Respuesta:**
```json
{
    "success": true,
    "criterios": {
        "Política de Cuotas": {
            "tipo": "alfabetico_apellido",
            "cambios_manuales": {}
        },
        ...
    }
}
```

#### GET `/api/desempate/criterio/<segmento_nombre>`
Obtiene el criterio para un segmento específico.

#### PUT `/api/desempate/criterio/<segmento_nombre>`
Actualiza el criterio automático.

**Body:**
```json
{
    "tipo_desempate": "alfabetico_apellido"
}
```

#### POST `/api/desempate/ordenamiento-manual/<segmento_nombre>`
Establece un ordenamiento manual completo.

**Body:**
```json
{
    "lista_ids": ["P001", "P002", "P003"]
}
```

#### POST `/api/desempate/cambio-manual/<segmento_nombre>`
Agrega un cambio manual individual.

**Body:**
```json
{
    "postulante_id": "P001",
    "posicion": 0
}
```

#### DELETE `/api/desempate/cambio-manual/<segmento_nombre>/<postulante_id>`
Remueve un cambio manual.

#### POST `/api/desempate/resetear/<segmento_nombre>`
Limpia todos los cambios manuales de un segmento.

## Persistencia

Los criterios de desempate se guardan en `data/criterios_desempate.json`:

```json
{
    "Política de Cuotas": {
        "segmento_nombre": "Política de Cuotas",
        "tipo_desempate": "alfabetico_apellido",
        "ordenamiento_manual": {},
        "fecha_actualizacion": "2024-01-19T10:30:45.123456"
    },
    ...
}
```

## Ejemplo de Uso

### Uso Programático

```python
from services.desempate_service import DesempateService
from domain.criterio_desempate import TipoDesempate

# Crear servicio
servicio = DesempateService()

# Cambiar criterio para un segmento
servicio.establecer_criterio_automatico(
    "Mérito Académico",
    TipoDesempate.MAYOR_EDAD
)

# Aplicar desempate
estudiantes_ordenados = servicio.aplicar_desempate(
    "Mérito Académico",
    estudiantes_con_misma_nota
)

# Cambio manual individual
servicio.agregar_cambio_manual(
    "Población General",
    postulante_id="P123",
    posicion=1
)
```

### Uso a través de API

```bash
# Obtener opciones
curl http://localhost:5000/api/desempate/opciones

# Cambiar criterio
curl -X PUT http://localhost:5000/api/desempate/criterio/Mérito\ Académico \
  -H "Content-Type: application/json" \
  -d '{"tipo_desempate": "mayor_edad"}'

# Agregar cambio manual
curl -X POST http://localhost:5000/api/desempate/cambio-manual/Población\ General \
  -H "Content-Type: application/json" \
  -d '{"postulante_id": "P123", "posicion": 1}'
```

## Interfaz de Usuario

La página de administración de desempates está disponible en `/desempates/gestionar` y proporciona:

1. **Tab de Criterios Automáticos**: 
   - Tabla mostrando criterio actual por segmento
   - Selector para cambiar a otro criterio
   - Explicación de cada opción disponible

2. **Tab de Cambios Manuales**:
   - Selector de segmento
   - Visualización de cambios manuales actuales
   - Formulario para agregar nuevos cambios
   - Botón para resetear todos los cambios

## Flujo de Desempate en la Asignación

1. Se ordena a los estudiantes por nota (descendente)
2. Se agrupan por nota
3. Para cada grupo con más de un estudiante:
   - Se consulta el servicio de desempate del segmento
   - Se aplica el criterio configurado
   - Si hay cambios manuales, estos se aplican primero
4. Se retorna la lista completa ordenada

## Campos Requeridos en Estudiante

Para que los criterios de desempate basados en edad funcionen, el objeto Estudiante debe incluir:

- `fecha_nacimiento`: datetime opcional
- `fecha_inscripcion`: datetime opcional

Estos campos se pueden cargar desde el archivo CSV de postulantes.

## Consideraciones de Diseño

### Inyección de Dependencias
El servicio de desempate se inyecta en las estrategias de asignación, permitiendo flexibilidad y facilidad de testing.

### Persistencia Automática
Los cambios se guardan automáticamente en JSON, permitiendo recuperación ante errores.

### Combinación Manual + Automática
Los cambios manuales tienen prioridad, pero si un postulante no está en el ordenamiento manual, se aplica el criterio automático.

### Extensibilidad
Es fácil agregar nuevos criterios de desempate extendiendo la enumeración `TipoDesempate` y añadiendo la lógica correspondiente en `_aplicar_criterio_automatico`.

## Próximas Mejoras Sugeridas

1. Auditoría de cambios (quién cambió qué y cuándo)
2. Vista previa de resultados antes de aplicar desempate
3. Desempate por criterios múltiples (por ejemplo: apellido, luego nombre)
4. Importación/exportación de configuraciones de desempate
5. Historial de cambios manuales
