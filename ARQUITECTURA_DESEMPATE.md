# Arquitectura del Sistema de Desempate

## Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────────┐
│                      CAPA PRESENTACIÓN                          │
├─────────────────────────────────────────────────────────────────┤
│  📱 templates/desempates/gestionar_desempates.html              │
│     - Tab: Criterios Automáticos                               │
│     - Tab: Cambios Manuales                                    │
│     - Interfaz web interactiva                                 │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     │ HTTP Requests/Responses
                     │
┌────────────────────▼────────────────────────────────────────────┐
│                      CAPA API REST                              │
├─────────────────────────────────────────────────────────────────┤
│  🔗 api/desempate_api.py (Flask Blueprint)                     │
│                                                                 │
│  ├─ GET    /api/desempate/opciones                            │
│  ├─ GET    /api/desempate/criterios                           │
│  ├─ GET    /api/desempate/criterio/<segmento>                │
│  ├─ PUT    /api/desempate/criterio/<segmento>                │
│  ├─ POST   /api/desempate/ordenamiento-manual/<segmento>     │
│  ├─ POST   /api/desempate/cambio-manual/<segmento>           │
│  ├─ DELETE /api/desempate/cambio-manual/<segmento>/<id>      │
│  └─ POST   /api/desempate/resetear/<segmento>                │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     │ Llamadas de Servicio
                     │
┌────────────────────▼────────────────────────────────────────────┐
│                   CAPA DE SERVICIO                              │
├─────────────────────────────────────────────────────────────────┤
│  ⚙️  services/desempate_service.py                             │
│                                                                 │
│  Responsabilidades:                                            │
│  ├─ Gestionar criterios por segmento                          │
│  ├─ Persistencia en JSON                                       │
│  ├─ Validación de datos                                        │
│  ├─ Orquestación de cambios                                   │
│  └─ Coordinación con Domain Layer                             │
│                                                                 │
│  Métodos principales:                                         │
│  ├─ obtener_criterio(segmento)                               │
│  ├─ establecer_criterio_automatico(seg, tipo)                │
│  ├─ establecer_ordenamiento_manual(seg, lista)               │
│  ├─ aplicar_desempate(seg, estudiantes)                      │
│  └─ (más métodos...)                                          │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     │ Usa
                     │
┌────────────────────▼────────────────────────────────────────────┐
│                   CAPA DOMINIO                                  │
├─────────────────────────────────────────────────────────────────┤
│  📦 domain/criterio_desempate.py                               │
│                                                                 │
│  ├─ Enum TipoDesempate                                        │
│  │  ├─ ALFABETICO_APELLIDO ✓                                 │
│  │  ├─ ALFABETICO_NOMBRE ✓                                   │
│  │  ├─ MAYOR_EDAD ✓                                          │
│  │  ├─ MENOR_EDAD ✓                                          │
│  │  ├─ FECHA_INSCRIPCION ✓                                   │
│  │  └─ MANUAL ✓                                              │
│  │                                                             │
│  └─ Clase CriterioDesempate                                  │
│     ├─ atributos:                                             │
│     │  ├─ segmento_nombre: str                               │
│     │  ├─ tipo_desempate: TipoDesempate                      │
│     │  ├─ ordenamiento_manual: Dict[id, posicion]            │
│     │  └─ fecha_actualizacion: datetime                      │
│     │                                                         │
│     └─ métodos:                                              │
│        ├─ aplicar_desempate(estudiantes)                    │
│        ├─ establecer_ordenamiento_manual(lista)             │
│        ├─ agregar_cambio_manual(id, pos)                   │
│        ├─ cambiar_criterio(tipo)                           │
│        ├─ to_dict() / from_dict()                          │
│        └─ (más métodos...)                                 │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     │ Consulta
                     │
┌────────────────────▼────────────────────────────────────────────┐
│                   MODELO DE DATOS                               │
├─────────────────────────────────────────────────────────────────┤
│  📄 domain/estudiante.py (actualizado)                         │
│                                                                 │
│  Campos adicionales:                                           │
│  ├─ fecha_nacimiento: datetime                               │
│  ├─ fecha_inscripcion: datetime                              │
│  └─ (campos existentes...)                                    │
└─────────────────────────────────────────────────────────────────┘
```

## Flujo de Integración con Asignación

```
┌─────────────────┐
│ Ejecutar        │
│ Asignación      │
└────────┬────────┘
         │
         ▼
┌──────────────────────────────────────────────┐
│ AsignadorCupos.__init__()                    │
│ (actualizado)                                │
│                                              │
│ 1. Recibe DesempateService                  │
│ 2. Inyecta en cada SegmentoStrategy          │
│    segmento.establecer_desempate_service()   │
└────────┬─────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────┐
│ Para cada Segmento:                          │
│                                              │
│ 1. Filtra estudiantes elegibles             │
│ 2. Ordena por nota (descendente)            │
│ 3. Llama _aplicar_desempate(estudiantes)    │
└────────┬─────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────┐
│ _aplicar_desempate():                        │
│                                              │
│ 1. Agrupa por nota                          │
│ 2. Para cada grupo con >1:                  │
│    - Consulta DesempateService              │
│    - Aplica desempate                       │
│ 3. Retorna estudiantes ordenados            │
└────────┬─────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────┐
│ DesempateService.aplicar_desempate():       │
│                                              │
│ 1. Obtiene CriterioDesempate del segmento  │
│ 2. Llama criterio.aplicar_desempate()       │
│ 3. Retorna estudiantes ordenados            │
└────────┬─────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────┐
│ CriterioDesempate.aplicar_desempate():      │
│                                              │
│ Lógica de Prioridad:                        │
│                                              │
│ SI hay cambios manuales:                    │
│   → Aplicar ordenamiento_manual             │
│   → Para no-manuales: aplicar criterio auto │
│                                              │
│ SINO:                                       │
│   → Aplicar criterio automático             │
│      (alfabético, edad, inscripción, etc)   │
└────────┬─────────────────────────────────────┘
         │
         ▼
    Retorna Lista Ordenada
```

## Persistencia de Datos

```
┌─────────────────────────────────────────────────┐
│   data/criterios_desempate.json                │
├─────────────────────────────────────────────────┤
│                                                 │
│  {                                             │
│    "Segmento 1": {                            │
│      "segmento_nombre": "Población General",  │
│      "tipo_desempate": "alfabetico_apellido", │
│      "ordenamiento_manual": {                 │
│        "P001": 2,                             │
│        "P003": 0,                             │
│        "P005": 1                              │
│      },                                       │
│      "fecha_actualizacion": "2026-01-19..."   │
│    },                                         │
│    "Segmento 2": { ... },                    │
│    ...                                        │
│  }                                            │
│                                                 │
└─────────────────────────────────────────────────┘
         ▲
         │
         │ Lee/Escribe
         │
    DesempateService
```

## Clases y Relaciones

```
┌─────────────────────┐
│  DesempateService   │
├─────────────────────┤
│ - criterios: Dict   │
│   key: nombre seg   │
│   val: Criterio     │
├─────────────────────┤
│ + obtener_criterio()│
│ + aplicar_desempate()
│ + (más métodos)     │
└──────────┬──────────┘
           │
    1..N   │ contiene
           │
           ▼
┌─────────────────────────────┐
│  CriterioDesempate          │
├─────────────────────────────┤
│ - segmento_nombre: str      │
│ - tipo_desempate: Enum      │
│ - ordenamiento_manual: Dict │
│ - fecha_actualizacion: dt   │
├─────────────────────────────┤
│ + aplicar_desempate()       │
│ + establecer_manual()       │
│ + cambiar_criterio()        │
│ + (más métodos)             │
└──────────┬──────────────────┘
           │
      usa  │
           ▼
┌─────────────────────────────┐
│  TipoDesempate (Enum)       │
├─────────────────────────────┤
│ - ALFABETICO_APELLIDO       │
│ - ALFABETICO_NOMBRE         │
│ - MAYOR_EDAD                │
│ - MENOR_EDAD                │
│ - FECHA_INSCRIPCION         │
│ - MANUAL                    │
└─────────────────────────────┘
```

## Integraciones

```
Componentes EXISTENTES           Nuevos Componentes
═════════════════════════════════════════════════════════════════

AsignadorCupos ←────────────────→ DesempateService
       │                               │
       ├─► Inyecta en Segmentos       │
       │                               │
       │  SegmentoAsignacionStrategy   │
       │  ├─ _aplicar_desempate() ◄───┘
       │  └─ (métodos existentes)
       │
       ├─► SegmentoMeritoAcademico
       ├─► SegmentoPoblacionGeneral
       ├─► (todos los segmentos)
       │   Ahora usan desempate ✓
       │
       └─► Retorna ResultadoAsignacion
           (con estudiantes ordenados)
```

## Estado de Completitud

```
✅ IMPLEMENTADO:
├─ Domain Layer (CriterioDesempate, TipoDesempate)
├─ Service Layer (DesempateService)
├─ API REST (desempate_api.py)
├─ Persistencia (JSON)
├─ Integración con AsignadorCupos
├─ Actualización de SegmentoAsignacionStrategy
├─ UI Web (gestionar_desempates.html)
├─ Pruebas (test_desempate.py)
├─ Documentación técnica
└─ Documentación de usuario

📋 PRÓXIMOS (Sugerencias):
├─ Sistema de auditoría
├─ Vista previa de resultados
├─ Importación/exportación
├─ Histórico de cambios
└─ Criterios personalizados
```

## Endpoints Disponibles

```
API REST para Desempate:

GET  /api/desempate/opciones
     → Retorna opciones disponibles

GET  /api/desempate/criterios
     → Retorna todos los criterios

GET  /api/desempate/criterio/<segmento>
     → Retorna criterio de un segmento

PUT  /api/desempate/criterio/<segmento>
     → Actualiza criterio automático
     Body: { "tipo_desempate": "valor" }

POST /api/desempate/ordenamiento-manual/<segmento>
     → Establece orden manual completo
     Body: { "lista_ids": ["P001", "P002", ...] }

POST /api/desempate/cambio-manual/<segmento>
     → Agrega cambio manual individual
     Body: { "postulante_id": "P001", "posicion": 0 }

DELETE /api/desempate/cambio-manual/<segmento>/<id>
       → Remueve cambio manual

POST /api/desempate/resetear/<segmento>
     → Limpia cambios manuales del segmento

Web UI:
GET  /desempates/gestionar
     → Interfaz web para gestión
```

---

**Última actualización**: 19 de Enero de 2026
