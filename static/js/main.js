// Utilidades generales para la aplicación Flask

/**
 * Función para hacer solicitudes GET
 */
function apiGet(url) {
    return fetch(url)
        .then(response => {
            if (!response.ok) throw new Error('Error en la solicitud');
            return response.json();
        });
}

/**
 * Función para hacer solicitudes POST
 */
function apiPost(url, data) {
    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) throw new Error('Error en la solicitud');
        return response.json();
    });
}

/**
 * Mostrar un modal
 */
function mostrarModal(id) {
    const modal = document.getElementById(id);
    if (modal) modal.classList.add('active');
}

/**
 * Cerrar un modal
 */
function cerrarModal(id) {
    const modal = document.getElementById(id);
    if (modal) modal.classList.remove('active');
}

/**
 * Mostrar notificación temporal
 */
function mostrarNotificacion(mensaje, tipo = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${tipo}`;
    alertDiv.textContent = mensaje;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
}

/**
 * Validar formulario antes de enviar
 */
function validarFormulario(formId) {
    const form = document.getElementById(formId);
    return form ? form.checkValidity() : false;
}

/**
 * Cargar períodos en un select
 */
function cargarPeriodosEnSelect(selectId) {
    fetch('{{ url_for("api_get_periodos") }}')
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById(selectId);
            if (select) {
                select.innerHTML = '<option value="">-- Selecciona un período --</option>';
                data.forEach(periodo => {
                    const option = document.createElement('option');
                    option.value = periodo.nombre;
                    option.textContent = periodo.nombre;
                    select.appendChild(option);
                });
            }
        })
        .catch(error => console.error('Error:', error));
}

/**
 * Formatear fecha a formato legible
 */
function formatearFecha(fecha) {
    if (!fecha) return '-';
    const date = new Date(fecha);
    return date.toLocaleDateString('es-ES');
}

/**
 * Confirmar antes de ejecutar acción
 */
function confirmar(mensaje = '¿Estás seguro de esta acción?') {
    return confirm(mensaje);
}

// Event listeners globales
document.addEventListener('DOMContentLoaded', function() {
    // Cerrar modales al hacer clic en el botón de cierre
    document.querySelectorAll('.modal-close').forEach(btn => {
        btn.addEventListener('click', function() {
            const modal = this.closest('.modal');
            if (modal) modal.classList.remove('active');
        });
    });

    // Cerrar modales al hacer clic fuera del contenido
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                this.classList.remove('active');
            }
        });
    });

    // Prevenir envío de formularios con validación
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!this.checkValidity()) {
                e.preventDefault();
                mostrarNotificacion('Por favor completa todos los campos requeridos', 'warning');
            }
        });
    });
});
