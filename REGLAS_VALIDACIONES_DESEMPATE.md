# Reglas de Negocio y Validaciones - Sistema de Desempate

## 📋 Reglas de Negocio

### Regla 1: Criterio por Segmento

**Descripción**: Cada segmento poblacional tiene su propio criterio de desempate independiente.

**Validación**:
- El sistema mantiene un criterio separado por segmento
- Cambiar el criterio de un segmento NO afecta otros
- Cada segmento puede tener diferente tipo de desempate

**Ejemplo**:
```
Población General → Mayor Edad
Vulnerabilidad → Alfabético Apellido  
Mérito Académico → Fecha Inscripción
```

### Regla 2: Desempate Solo en Empates

**Descripción**: El desempate se aplica SOLO cuando hay dos o más estudiantes con la misma nota.

**Validación**:
- Nota diferente = No se aplica desempate
- Una persona con esa nota = No se aplica desempate
- Múltiples con misma nota = Se aplica desempate

**Ejemplo**:
```
Nota 85.5 → P001, P002, P003 (3 estudiantes)
→ Se aplica desempate entre los 3

Nota 85.5 → P001 (1 estudiante)
→ No se aplica desempate

Nota 85.0 → P001 (diferente)
Nota 85.5 → P002, P003 (empate entre 2)
→ Se aplica desempate solo entre P002 y P003
```

### Regla 3: Prioridad Manual > Automática

**Descripción**: Los cambios manuales siempre tienen prioridad sobre criterios automáticos.

**Validación**:
- Si hay cambio manual → Se aplica primero
- Si no hay manual → Se aplica criterio automático
- Cambios manuales pueden ser parciales (no todos los postulantes)

**Ejemplo**:
```
Criterio: Alfabético Apellido
Postulantes: P001=Avellaneda, P002=Benítez, P003=Chamorro

Sin cambio manual:
1. Avellaneda (A)
2. Benítez (B)
3. Chamorro (C)

Con cambio manual (P002 → posición 0):
1. Benítez (cambio manual)
2. Avellaneda (criterio automático)
3. Chamorro (criterio automático)
```

### Regla 4: Persistencia Automática

**Descripción**: Todos los cambios se guardan automáticamente en JSON.

**Validación**:
- Cambio inmediato en archivo
- Sin intervención del usuario
- Sin necesidad de confirmar guardar
- Se recuperan al reiniciar

**Archivos**:
```
data/criterios_desempate.json
```

### Regla 5: Independencia de Asignación

**Descripción**: El desempate se aplica DURANTE la asignación, no antes.

**Validación**:
- No se modifica datos de postulantes
- No se guarda resultado de desempate
- Se recalcula en cada ejecución
- Cambios de criterio se aplican en próxima asignación

**Flujo**:
```
Usuario cambia criterio
    ↓
Se guarda en JSON
    ↓
Usuario ejecuta asignación
    ↓
Sistema carga criterios desde JSON
    ↓
Se aplica desempate dinámicamente
    ↓
Se generan resultados
```

## ✅ Validaciones de Entrada

### Validación 1: ID de Postulante

**Requisitos**:
- ✅ No puede estar vacío
- ✅ Debe ser string alfanumérico
- ✅ Máximo 20 caracteres

**Ejemplo válido**: `P001`, `EST123`, `UNIV_001`
**Ejemplo inválido**: `""`, `!@#$`, `POSTULANTE_NUMERO_MUY_LARGO_PARA_LOS_LÍMITES`

### Validación 2: Posición en Ordenamiento Manual

**Requisitos**:
- ✅ Debe ser número entero
- ✅ Debe ser >= 0
- ✅ No tiene límite máximo (pueden haber más postulantes)

**Ejemplo válido**: `0`, `1`, `10`, `999`
**Ejemplo inválido**: `-1`, `3.5`, `abc`, `null`

### Validación 3: Tipo de Desempate

**Requisitos**:
- ✅ Debe ser uno de los tipos válidos
- ✅ Case-sensitive
- ✅ No puede estar vacío

**Valores válidos**:
```
"alfabetico_apellido"
"alfabetico_nombre"
"mayor_edad"
"menor_edad"
"fecha_inscripcion"
"manual"
```

**Valores inválidos**:
```
"Alfabetico_Apellido" (mayúsculas)
"alfabetico apellido" (espacios)
"otra_opcion"
""
null
```

### Validación 4: Nombre de Segmento

**Requisitos**:
- ✅ Debe existir en el sistema
- ✅ Debe coincidir exactamente
- ✅ Case-sensitive

**Segmentos válidos**:
```
"Política de Cuotas"
"Vulnerabilidad"
"Mérito Académico"
"Otros Méritos"
"Bachilleres Pueblos Nacionalidades"
"Bachilleres Generales"
"Población General"
```

## 🔒 Restricciones

### Restricción 1: Un Criterio por Segmento

- Solo UN criterio activo a la vez por segmento
- Cambiar criterio reemplaza el anterior
- No se pueden combinar criterios

### Restricción 2: Posiciones Únicas

- La misma posición puede tener múltiples postulantes
- El sistema ordena alfabéticamente en caso de empate de posición
- No hay conflicto, es válido

**Ejemplo**:
```
P001 → Posición 0
P002 → Posición 0
P003 → Posición 1

Resultado:
1. P001 (por alfabeto vs P002)
2. P002 (por alfabeto vs P001)
3. P003 (posición 1)
```

### Restricción 3: Cambios Manuales Parciales

- No es necesario listar todos los postulantes
- Los no listados se ordena con criterio automático
- No hay problema de postulantes "faltantes"

### Restricción 4: Cambios Solo en Segmentos Existentes

- No se pueden crear segmentos nuevos
- Solo se pueden modificar los 7 segmentos predefinidos
- Cualquier otro segmento devuelve error 404

## ⚠️ Casos de Error

### Error 1: Segmento No Encontrado

```
GET /api/desempate/criterio/SegmentoInventado
↓
{
    "success": false,
    "error": "Segmento SegmentoInventado no encontrado"
}
Status: 404
```

**Solución**: Usar uno de los 7 segmentos válidos

### Error 2: Tipo de Desempate Inválido

```
PUT /api/desempate/criterio/Población General
Body: { "tipo_desempate": "criterio_inexistente" }
↓
{
    "success": false,
    "error": "Tipo de desempate inválido: criterio_inexistente"
}
Status: 400
```

**Solución**: Usar un tipo válido de la lista

### Error 3: Parámetros Faltantes

```
POST /api/desempate/cambio-manual/Población General
Body: { "postulante_id": "P001" }  ← Falta "posicion"
↓
{
    "success": false,
    "error": "postulante_id y posicion son requeridos"
}
Status: 400
```

**Solución**: Incluir todos los parámetros requeridos

### Error 4: Formato JSON Inválido

```
POST /api/desempate/ordenamiento-manual/Población General
Body: { "lista_ids": "P001, P002" }  ← Es string, debe ser array
↓
{
    "success": false,
    "error": "lista_ids es requerido y debe ser una lista"
}
Status: 400
```

**Solución**: Enviar array JSON válido

## 🔄 Estados Válidos

### Estado 1: Sin Cambios Manuales

```json
{
    "tipo_desempate": "alfabetico_apellido",
    "ordenamiento_manual": {}
}
↓
Comportamiento: Usa criterio automático
```

### Estado 2: Con Cambios Manuales

```json
{
    "tipo_desempate": "manual",
    "ordenamiento_manual": {
        "P001": 0,
        "P003": 1
    }
}
↓
Comportamiento:
- P001 va primero
- P003 va segundo
- Los demás: criterio automático
```

### Estado 3: Cambios Manuales + Criterio Automático

```json
{
    "tipo_desempate": "mayor_edad",
    "ordenamiento_manual": {
        "P001": 0
    }
}
↓
Comportamiento:
- P001 va primero (manual)
- Otros: ordenados por edad (automático)
```

## 📊 Matriz de Validación

| Campo | Tipo | Requerido | Rango | Válido |
|-------|------|-----------|-------|--------|
| segmento | String | ✓ | 7 opciones | ✓ |
| tipo_desempate | String | ✓ | 6 tipos | ✓ |
| postulante_id | String | ✓ | 1-20 chars | ✓ |
| posicion | Integer | ✓ | >= 0 | ✓ |
| lista_ids | Array | ✓ | String[] | ✓ |

## 🧪 Pruebas de Validación

### Test 1: ID Postulante Vacío

```python
def test_id_vacio():
    with pytest.raises(ValueError):
        servicio.agregar_cambio_manual(
            "Población General",
            "",  # ❌ Error
            0
        )
```

### Test 2: Posición Negativa

```python
def test_posicion_negativa():
    with pytest.raises(ValueError):
        servicio.agregar_cambio_manual(
            "Población General",
            "P001",
            -1  # ❌ Error
        )
```

### Test 3: Tipo Desempate Inválido

```python
def test_tipo_invalido():
    with pytest.raises(ValueError):
        servicio.establecer_criterio_automatico(
            "Población General",
            "criterio_inexistente"  # ❌ Error
        )
```

## 📝 Logs y Auditoría

### Información Registrada

```
✅ Cambios de criterios automáticos
✅ Cambios manuales agregados/removidos
✅ Reseteos de segmentos
❌ NO se registra: datos personales de postulantes
❌ NO se registra: contraseñas
```

### Dónde se Registra

```
data/criterios_desempate.json
└─ "fecha_actualizacion": "2026-01-19T20:37:45.816199"
```

## 🎯 Regla de Oro

> **"Los cambios manuales siempre tienen prioridad,**
> **pero el sistema debe ser predecible y auditables."**

Esto significa:
- ✅ Admin tiene control total
- ✅ El sistema es automático cuando no hay manual
- ✅ Todo se guarda y es recuperable
- ✅ Cambios son reversibles
