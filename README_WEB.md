# SAC - Sistema de Asignación de Cupos (Versión Web)

¡Tu aplicación ha sido completamente migrada de Tkinter a Flask con todas las funcionalidades integradas!

## 🚀 Cómo Usar

### 1. **Iniciar el Servidor**

```bash
python app.py
```

Esto iniciará el servidor en `http://127.0.0.1:5000`

### 2. **Acceder a la Aplicación**

Abre tu navegador web e ingresa:
```
http://localhost:5000
```

### 3. **Credenciales de Prueba**

- **Usuario:** admin
- **Contraseña:** admin123

---

## 📁 Estructura del Proyecto

```
├── app.py                          # Aplicación Flask completa (✓ COMPLETADA)
├── main.py                         # Script original (ya no necesario)
├── templates/                      # Templates HTML
│   ├── base.html                   # Template base (heredan los demás)
│   ├── login.html                  # Página de login
│   ├── menu.html                   # Menú principal
│   ├── periodos/                   # ✓ Templates de períodos FUNCIONALES
│   ├── carreras/                   # ✓ Templates de carreras FUNCIONALES
│   ├── ofertas/                    # ✓ Templates de ofertas FUNCIONALES
│   ├── postulantes/                # ✓ Templates de postulantes FUNCIONALES
│   ├── resultados/                 # ✓ Templates de resultados FUNCIONALES
│   └── estadisticas/               # ✓ Templates de estadísticas FUNCIONALES
├── static/                         # Archivos estáticos
│   ├── css/
│   │   └── style.css               # Estilos CSS
│   └── js/
│       └── main.js                 # JavaScript principal
├── domain/                         # Clases del dominio (sin cambios)
├── services/                       # Servicios (sin cambios)
└── patterns/                       # Patrones de diseño (sin cambios)
```

---

## ✨ Funcionalidades COMPLETADAS

### ✅ Autenticación
- ✓ Login con validación de credenciales
- ✓ Sesiones de usuario
- ✓ Logout

### ✅ Períodos (100% funcional)
- ✓ Listar períodos
- ✓ Crear nuevo período
- ✓ Activar período
- ✓ Eliminar período
- ✓ Integración con `PeriodoService`

### ✅ Carreras/Ofertas (100% funcional)
- ✓ Ver ofertas académicas
- ✓ Crear nueva carrera
- ✓ Listar carreras con cupos
- ✓ Conteo de inscritos por carrera
- ✓ Integración con `OfertaAcademicaService`

### ✅ Postulantes (100% funcional)
- ✓ Cargar postulantes desde CSV
- ✓ Cargar postulantes desde Excel (XLSX)
- ✓ Validación de archivos
- ✓ Listar postulantes cargados
- ✓ Integración con `PostulanteService`

### ✅ Asignación de Cupos (100% funcional)
- ✓ Ejecutar proceso de asignación
- ✓ Validación de datos requeridos
- ✓ Mensajes de error claros
- ✓ Integración con `AsignacionService`

### ✅ Resultados (100% funcional)
- ✓ Ver resultados de asignación
- ✓ Mostrar estado de cada postulante
- ✓ Exportar resultados a CSV
- ✓ Exportar resultados a Excel
- ✓ Integración con `AsignacionService`

### ✅ Estadísticas (100% funcional)
- ✓ Total de postulantes
- ✓ Cantidad de asignados
- ✓ Cantidad de no asignados
- ✓ Tasa de asignación (porcentaje)
- ✓ Resumen por carrera
- ✓ Integración con estadísticas en tiempo real

---

## 🔧 Cambios Realizados

### De Tkinter a Flask:

| Tkinter | Flask | Estado |
|---------|-------|--------|
| `VentanaBase(tk.Toplevel)` | `@app.route('/ruta')` | ✓ |
| Buttons → Enlaces | `<a href>` y `<button>` | ✓ |
| Entry widgets | `<input type="text">` | ✓ |
| Message boxes | Alerts CSS + Flash messages | ✓ |
| Canvas/widgets | HTML + CSS | ✓ |
| Obtener datos | APIs JSON | ✓ |

### APIs Creadas:

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/periodos` | GET | Obtiene lista de períodos |
| `/api/periodos/<nombre>/activar` | POST | Activa un período |
| `/api/periodos/<nombre>/eliminar` | POST | Elimina un período |
| `/api/ofertas` | GET | Obtiene ofertas académicas |
| `/api/postulantes` | GET | Obtiene postulantes cargados |
| `/api/resultados` | GET | Obtiene resultados de asignación |
| `/api/estadisticas` | GET | Obtiene estadísticas en tiempo real |

---

## 📚 Flujo de Trabajo Completo

### Paso 1: Crear un Período
1. Ir a **Períodos** → **+ Nuevo Período**
2. Ingresar nombre (ej: "2025-1")
3. Seleccionar fechas de inicio y fin
4. El período se crea y activa automáticamente

### Paso 2: Configurar Carreras
1. Ir a **Carreras**
2. Llenar el formulario con:
   - Nombre de la carrera
   - Sigla (código)
   - Número de cupos
3. Las carreras se guardan en la oferta académica del período

### Paso 3: Cargar Postulantes
1. Ir a **Postulantes** → **Cargar**
2. Seleccionar archivo CSV o Excel
3. El sistema valida y carga automáticamente

### Paso 4: Ejecutar Asignación
1. Ir a **Asignación**
2. Verificar que el período está activo
3. Hacer clic en **Ejecutar Asignación**
4. El sistema ejecuta el algoritmo de asignación

### Paso 5: Ver Resultados
1. Ir a **Resultados**
2. Se muestra tabla con todos los asignados
3. Exportar en CSV o Excel si es necesario

### Paso 6: Analizar Estadísticas
1. Ir a **Estadísticas**
2. Se muestran métricas en tiempo real
3. Resumen por carrera

---

## 💡 Formato de Archivos

### CSV para Postulantes

El archivo CSV debe tener las siguientes columnas:

```
id_postulante,correo,num_telefono,nombres,apellidos,nota_postulacion,opcion_1,politica_cuotas,vulnerable,cuadro_honor,pueblo_nacionalidad,titulo_superior,otro_merito
```

**Ejemplo:**
```
1001,juan@email.com,1234567890,Juan,Pérez,95.5,INF,0,1,0,0,0,0
1002,maria@email.com,0987654321,María,García,88.0,ICI,1,0,1,0,0,0
```

### Excel para Postulantes

Mismo formato anterior pero en hoja Excel (XLSX).

---

## 🎨 Personalización

### Cambiar Colores
Edita `/static/css/style.css`:
```css
:root {
    --primary: #667eea;      /* Cambiar este color */
    --secondary: #764ba2;
    ...
}
```

### Cambiar Logo/Título
Edita `templates/base.html`:
```html
<div class="navbar-brand">SAC</div>  <!-- Cambiar aquí -->
```

### Agregar Nueva Página

1. Crea template en `templates/nueva_pagina.html`
2. Agrega ruta en `app.py`:
   ```python
   @app.route('/nueva-pagina')
   @verificar_autenticacion
   def nueva_pagina():
       return render_template('nueva_pagina.html')
   ```
3. Agrega enlace en `templates/base.html`

---

## 🐛 Solución de Problemas

### Puerto 5000 ya está en uso
```bash
# En app.py, cambiar la última línea a:
app.run(debug=True, host='127.0.0.1', port=8000)
```

### Error "Período no activo"
- Asegúrate de crear y activar un período antes de cargar postulantes
- Cada acción requiere un período activo

### Error al cargar archivos
- Verifica que el archivo es CSV o XLSX
- Asegúrate que tiene todas las columnas requeridas
- Los datos deben estar en el formato correcto

### No aparecen datos en tablas
- Recarga la página (F5)
- Verifica la consola del navegador (F12) para errores

---

## 📦 Dependencias Instaladas

```
flask==3.1.2
flask-cors==6.0.2
pandas==2.3.3
openpyxl==3.1.5
werkzeug==3.1.5
```

Para instalar manualmente:
```bash
pip install flask flask-cors pandas openpyxl
```

---

## 🚀 Deployment (Producción)

Para usar en producción, reemplaza Flask con Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Cambios recomendados en `app.py`:
```python
app.secret_key = 'CAMBIA_ESTO_POR_UNA_CLAVE_SEGURA_ALEATORIA'
app.run(debug=False)  # Deshabilitar debug en producción
```

---

## 📝 Notas Importantes

1. **Integridad de Datos**: Todos los datos se guardan en la carpeta `data/`
2. **Períodos**: El sistema maneja un período activo a la vez
3. **Backups**: Realiza backups de la carpeta `data/` regularmente
4. **Seguridad**: Cambia la clave secreta en producción
5. **Performance**: Para más de 10,000 postulantes, considera usar una base de datos

---

## 🎯 Próximas Mejoras Opcionales

- [ ] Sistema de base de datos (SQLAlchemy)
- [ ] Autenticación LDAP/Active Directory
- [ ] Reportes PDF avanzados
- [ ] Gráficos interactivos (Chart.js)
- [ ] Sistema de auditoría de cambios
- [ ] API REST para integraciones externas
- [ ] Soporte multi-idioma

---

**¡Tu aplicación web está 100% operacional! 🎉**

Cualquier duda, revisa los comentarios en el código o consulta la documentación de los servicios.

