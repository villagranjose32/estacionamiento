// JavaScript principal para el Sistema de Estacionamiento

// Configuración global
const CONFIG = {
    API_BASE: '',
    UPDATE_INTERVAL: 30000, // 30 segundos
    ANIMATION_DURATION: 300
};

// Utilidades
const Utils = {
    // Formatear moneda
    formatCurrency: (amount) => {
        return new Intl.NumberFormat('es-CO', {
            style: 'currency',
            currency: 'COP',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(amount);
    },

    // Formatear tiempo
    formatTime: (seconds) => {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        return `${hours}h ${minutes}m`;
    },

    // Mostrar notificación
    showNotification: (message, type = 'info') => {
        const alertClass = type === 'success' ? 'alert-success' : 
                          type === 'error' ? 'alert-danger' : 
                          type === 'warning' ? 'alert-warning' : 'alert-info';
        
        const notification = document.createElement('div');
        notification.className = `alert ${alertClass} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove después de 5 segundos
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    },

    // Validar placa
    validatePlaca: (placa) => {
        const regex = /^[A-Z0-9-]{3,8}$/;
        return regex.test(placa.toUpperCase());
    },

    // Debounce para optimizar llamadas a funciones
    debounce: (func, wait) => {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};

// Clase principal para la gestión del dashboard
class EstacionamientoDashboard {
    constructor() {
        this.updateInterval = null;
        this.init();
    }

    init() {
        this.bindEvents();
        this.startAutoUpdate();
        this.initializeFormValidation();
    }

    bindEvents() {
        // Botón de actualización manual
        const btnActualizar = document.getElementById('btn-actualizar');
        if (btnActualizar) {
            btnActualizar.addEventListener('click', () => {
                this.updateDashboard();
            });
        }

        // Formularios
        this.initializeFormHandlers();
    }

    initializeFormHandlers() {
        // Formulario de ingreso
        const formIngreso = document.querySelector('form[action*="ingresar"]');
        if (formIngreso) {
            formIngreso.addEventListener('submit', (e) => {
                const placa = formIngreso.querySelector('input[name="placa"]').value;
                if (!Utils.validatePlaca(placa)) {
                    e.preventDefault();
                    Utils.showNotification('Formato de placa inválido. Use entre 3-8 caracteres alfanuméricos.', 'error');
                }
            });
        }

        // Auto-uppercase para campos de placa
        document.querySelectorAll('input[name="placa"]').forEach(input => {
            input.addEventListener('input', (e) => {
                e.target.value = e.target.value.toUpperCase();
            });
        });
    }

    async updateDashboard() {
        try {
            const response = await fetch('/api/estado');
            if (!response.ok) throw new Error('Error al obtener datos');
            
            const data = await response.json();
            this.updateDashboardStats(data);
            
            // Actualizar tabla de vehículos si existe
            if (document.getElementById('tabla-vehiculos')) {
                await this.updateVehiculosTable();
            }
            
        } catch (error) {
            console.error('Error actualizando dashboard:', error);
            Utils.showNotification('Error al actualizar los datos', 'error');
        }
    }

    updateDashboardStats(data) {
        // Actualizar estadísticas
        const elementos = {
            'espacios-disponibles': data.disponibles,
            'espacios-ocupados': data.ocupados,
            'porcentaje-ocupacion': data.porcentaje_ocupacion.toFixed(1) + '%'
        };

        Object.entries(elementos).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                // Animación de cambio de valor
                element.style.transform = 'scale(1.1)';
                setTimeout(() => {
                    element.textContent = value;
                    element.style.transform = 'scale(1)';
                }, 150);
            }
        });

        // Actualizar barra de progreso
        const barra = document.getElementById('barra-ocupacion');
        if (barra) {
            barra.style.width = data.porcentaje_ocupacion + '%';
            barra.textContent = data.porcentaje_ocupacion.toFixed(1) + '%';
            
            // Cambiar color según ocupación
            barra.className = 'progress-bar';
            if (data.porcentaje_ocupacion > 80) {
                barra.classList.add('bg-danger');
            } else if (data.porcentaje_ocupacion > 60) {
                barra.classList.add('bg-warning');
            } else {
                barra.classList.add('bg-success');
            }
        }
    }

    async updateVehiculosTable() {
        try {
            const response = await fetch('/api/vehiculos');
            if (!response.ok) throw new Error('Error al obtener vehículos');
            
            const vehiculos = await response.json();
            const tbody = document.querySelector('#tabla-vehiculos tbody');
            
            if (!tbody) return;
            
            // Limpiar tabla
            tbody.innerHTML = '';
            
            if (vehiculos.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="8" class="text-center py-4">
                            <i class="fas fa-car fa-2x text-muted mb-2"></i>
                            <br>No hay vehículos en el estacionamiento
                        </td>
                    </tr>
                `;
                return;
            }
            
            // Agregar vehículos
            vehiculos.forEach(vehiculo => {
                const abonoHtml = vehiculo.tiene_abono 
                    ? '<span class="badge bg-success" title="Con descuento del 10%"><i class="fas fa-calendar-check"></i> Sí</span>'
                    : '<span class="badge bg-secondary"><i class="fas fa-times"></i> No</span>';
                
                const tarifaHtml = vehiculo.tiene_abono 
                    ? `<span class="badge bg-success">${Utils.formatCurrency(vehiculo.tarifa_actual)} <small class="text-muted">(-10%)</small></span>`
                    : `<span class="badge bg-success">${Utils.formatCurrency(vehiculo.tarifa_actual)}</span>`;
                
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td><strong>${vehiculo.placa}</strong></td>
                    <td><span class="badge bg-secondary">${vehiculo.tipo}</span></td>
                    <td>${vehiculo.propietario || 'No especificado'}</td>
                    <td><span class="badge bg-info">${vehiculo.espacio}</span></td>
                    <td>${vehiculo.hora_entrada}</td>
                    <td>${vehiculo.tiempo_horas}h ${vehiculo.tiempo_minutos}m</td>
                    <td>${abonoHtml}</td>
                    <td>${tarifaHtml}</td>
                `;
                tbody.appendChild(row);
            });
            
        } catch (error) {
            console.error('Error actualizando tabla de vehículos:', error);
        }
    }

    startAutoUpdate() {
        // Actualizar cada 30 segundos
        this.updateInterval = setInterval(() => {
            this.updateDashboard();
        }, CONFIG.UPDATE_INTERVAL);
    }

    stopAutoUpdate() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }
    }

    initializeFormValidation() {
        // Validación en tiempo real para formularios
        document.querySelectorAll('form').forEach(form => {
            form.addEventListener('submit', (e) => {
                const isValid = this.validateForm(form);
                if (!isValid) {
                    e.preventDefault();
                }
            });
        });
    }

    validateForm(form) {
        let isValid = true;
        const requiredFields = form.querySelectorAll('[required]');
        
        requiredFields.forEach(field => {
            const value = field.value.trim();
            const fieldContainer = field.closest('.mb-3') || field.parentElement;
            
            // Remover mensajes de error previos
            const existingError = fieldContainer.querySelector('.error-message');
            if (existingError) {
                existingError.remove();
            }
            
            field.classList.remove('is-invalid');
            
            if (!value) {
                this.showFieldError(field, 'Este campo es obligatorio');
                isValid = false;
            } else if (field.name === 'placa' && !Utils.validatePlaca(value)) {
                this.showFieldError(field, 'Formato de placa inválido');
                isValid = false;
            }
        });
        
        return isValid;
    }

    showFieldError(field, message) {
        field.classList.add('is-invalid');
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message text-danger small mt-1';
        errorDiv.textContent = message;
        field.parentElement.appendChild(errorDiv);
    }
}

// Clase para gestionar el simulador de tarifas
class TarifaSimulator {
    constructor() {
        this.initSimulator();
    }

    initSimulator() {
        const simTipo = document.getElementById('sim-tipo');
        const simHoras = document.getElementById('sim-horas');
        
        if (simTipo && simHoras) {
            [simTipo, simHoras].forEach(element => {
                element.addEventListener('change', () => this.calculate());
                element.addEventListener('input', Utils.debounce(() => this.calculate(), 300));
            });
            
            // Agregar listeners a los inputs de tarifas
            document.querySelectorAll('input[name^="tarifa_"]').forEach(input => {
                input.addEventListener('input', Utils.debounce(() => this.calculate(), 300));
            });
            
            this.calculate();
        }
    }

    calculate() {
        const tipo = document.getElementById('sim-tipo').value;
        const horas = parseFloat(document.getElementById('sim-horas').value) || 0;
        
        const tarifaInput = document.getElementById('tarifa_' + tipo);
        const tarifaPorHora = parseInt(tarifaInput.value) || 0;
        
        const horasACobrar = Math.max(1, Math.ceil(horas));
        const total = horasACobrar * tarifaPorHora;
        
        const resultElement = document.getElementById('sim-resultado');
        if (resultElement) {
            resultElement.textContent = `${Utils.formatCurrency(total)} (${horasACobrar} horas)`;
        }
    }
}

// Inicialización cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar dashboard si estamos en la página principal
    if (document.getElementById('espacios-disponibles')) {
        new EstacionamientoDashboard();
    }
    
    // Inicializar simulador de tarifas si existe
    if (document.getElementById('sim-tipo')) {
        new TarifaSimulator();
    }
    
    // Inicializar tooltips de Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Animar elementos al cargar
    document.querySelectorAll('.card').forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Configurar auto-dismiss para alertas
    document.querySelectorAll('.alert').forEach(alert => {
        if (!alert.querySelector('.btn-close')) return;
        
        setTimeout(() => {
            if (alert.parentNode) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000);
    });
});

// Manejar visibilidad de la página para pausar/reanudar actualizaciones
document.addEventListener('visibilitychange', function() {
    const dashboard = window.estacionamientoDashboard;
    if (dashboard) {
        if (document.hidden) {
            dashboard.stopAutoUpdate();
        } else {
            dashboard.startAutoUpdate();
            dashboard.updateDashboard(); // Actualizar inmediatamente al volver
        }
    }
});

// Exportar utilidades para uso global
window.EstacionamientoUtils = Utils;