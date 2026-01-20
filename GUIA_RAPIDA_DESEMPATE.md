# Guía Rápida de Inicio - Sistema de Desempate

## 🚀 Inicio Rápido (3 pasos)

### 1. Acceder a la Interfaz

```
URL: http://localhost:5000/desempates/gestionar
Usuario: admin
Clave: admin123
```

### 2. Ver y Cambiar Criterios

**Pestaña: Criterios Automáticos**

- Verás una tabla con todos los segmentos
- Cada segmento muestra su criterio actual
- Usa el dropdown para cambiar a otro criterio
- Cambios se guardan automáticamente ✅

### 3. Agregar Cambios Manuales

**Pestaña: Cambios Manuales**

1. Selecciona un segmento del dropdown
2. Verás los cambios manuales actuales (si hay)
3. Completa el formulario:
   - **ID Postulante**: ej. "P001"
   - **Posición**: 0 = primero, 1 = segundo, etc.
4. Click en "Agregar Cambio"

## 📊 Opciones de Desempate

| Opción | Uso | Ejemplo |
|--------|-----|---------|
| 🔤 Alfabético Apellido | Por defecto, ordenamiento A-Z | Avellaneda, Benítez, Chamorro |
| 🔤 Alfabético Nombre | Ordenamiento por nombre A-Z | Ana, Carlos, Juan |
| 👴 Mayor Edad | Favorece a los más mayores | Nacido 1998 > 1999 > 2000 |
| 👶 Menor Edad | Favorece a los más jóvenes | Nacido 2000 > 1999 > 1998 |
| 📅 Fecha Inscripción | Orden de inscripción FIFO | Inscrito 9:00 > 10:00 > 11:00 |

## 💡 Ejemplos Prácticos

### Ejemplo 1: Cambiar Criterio para "Población General"

```
1. Entra a /desempates/gestionar
2. Tab: "Criterios Automáticos"
3. Busca "Población General" en la tabla
4. Click en dropdown → Selecciona "Mayor Edad"
5. ¡Listo! El cambio se guarda automáticamente
```

### Ejemplo 2: Priorizar un Postulante

```
1. Tab: "Cambios Manuales"
2. Dropdown: Selecciona "Población General"
3. Ingresa:
   - ID Postulante: P001
   - Posición: 0
4. Click "Agregar Cambio"
5. P001 será asignado primero si hay empate

Nota: Posición 0 = Primero
      Posición 1 = Segundo
      Posición 2 = Tercero, etc.
```

### Ejemplo 3: Remover un Cambio Manual

```
1. Tab: "Cambios Manuales"
2. Selecciona segmento que contiene el cambio
3. En la lista de "Cambios Manuales Actuales"
4. Click "Remover" al lado del postulante
5. ¡Removido! El sistema usará criterio automático
```

## 🔧 Resetear Todo

### Resetear Cambios de un Segmento

```
1. Tab: "Cambios Manuales"
2. Selecciona segmento
3. Click rojo: "Resetear Cambios Manuales"
4. Confirma en el dialog
5. ¡Todos los cambios del segmento se eliminan!
```

## 📱 Uso Programático (API)

### Cambiar Criterio

```bash
curl -X PUT http://localhost:5000/api/desempate/criterio/Población\ General \
  -H "Content-Type: application/json" \
  -d '{"tipo_desempate": "mayor_edad"}'
```

### Agregar Cambio Manual

```bash
curl -X POST http://localhost:5000/api/desempate/cambio-manual/Población\ General \
  -H "Content-Type: application/json" \
  -d '{"postulante_id": "P001", "posicion": 0}'
```

### Ver Criterios

```bash
curl http://localhost:5000/api/desempate/criterios
```

## ⚠️ Casos Comunes

### ¿Qué pasa si hay empate?

```
Estudiantes con nota 85.5:
- P001: Juan Avellaneda
- P002: Ana Benítez
- P003: Carlos Chamorro

Con criterio "Alfabético Apellido":
1. Juan Avellaneda ← A es primera
2. Ana Benítez ← B es segunda
3. Carlos Chamorro ← C es tercera
```

### ¿Cómo funciona la prioridad?

```
Prioridad en Desempate:

1. ✅ Cambios Manuales (MÁXIMA)
   → Si P001 está en posición 0 → va primero
   
2. Criterio Automático (si no hay manual)
   → Por orden: alfabético/edad/inscripción
   
3. Nota: Todos tienen MISMA nota en mismo segmento
   → Por eso necesitan desempate
```

### ¿Se pierde al reiniciar?

```
❌ NO. Los criterios se guardan en:
   data/criterios_desempate.json

✅ Se recuperan automáticamente
   al reiniciar la aplicación
```

## 🐛 Troubleshooting

### Cambios no se guardan

```
✅ Solución:
- Verifica que estés autenticado
- Revisa la consola del navegador (F12)
- Asegúrate que la URL es /desempates/gestionar
```

### No veo la página

```
✅ Solución:
- Verifica que el servidor está corriendo
- Prueba: http://localhost:5000
- Si no funciona, reinicia la aplicación
```

### Los cambios no se aplican

```
✅ Solución:
- Los cambios se aplican en la PRÓXIMA asignación
- Ejecuta asignación nuevamente
- Mira los resultados
```

## 📚 Documentación Completa

Para más detalles:

- **`SISTEMA_DESEMPATE.md`** - Guía completa
- **`DESEMPATE_DOCUMENTACION.md`** - Referencia técnica
- **`ARQUITECTURA_DESEMPATE.md`** - Diagramas

## ✅ Checklist de Funcionalidades

- ✅ Ver criterios actuales
- ✅ Cambiar criterio automático
- ✅ Ver cambios manuales
- ✅ Agregar cambios manuales
- ✅ Remover cambios individuales
- ✅ Resetear todos los cambios
- ✅ Persistencia automática
- ✅ Aplicación en asignación

## 🎯 Próximos Pasos

1. **Prueba el sistema**
   ```bash
   python tests/test_desempate.py
   ```

2. **Accede a la interfaz**
   ```
   http://localhost:5000/desempates/gestionar
   ```

3. **Experimenta con criterios**
   - Cambia entre opciones
   - Agrega cambios manuales
   - Resetea y prueba de nuevo

4. **Ejecuta asignación**
   - Ve si los desempates se aplican
   - Verifica los resultados

---

**¡Listo! Ya puedes usar el sistema de desempates. 🚀**

Para ayuda: Consulta la documentación en los archivos .md del proyecto
