# 🚗 Sistema de Gestión de Estacionamiento

Un sistema completo y moderno para gestionar el ingreso y egreso de vehículos en un estacionamiento, con interfaz web responsive y funcionalidades avanzadas.

## ✨ Características Principales

- 🚗 **Gestión de Vehículos**: Registro completo de ingreso y egreso
- 💰 **Cálculo Automático**: Tarifas por tiempo de permanencia
- 🎫 **Abonos Mensuales**: Sistema de suscripciones con 10% de descuento
- 📊 **Dashboard en Tiempo Real**: Estadísticas y monitoreo instantáneo  
- 🌐 **Interfaz Web Moderna**: Diseño responsive con Bootstrap 5
- 📱 **Multi-dispositivo**: Acceso desde PC, tablet y móviles
- ⚡ **Egreso Rápido**: Botones de egreso individual desde el dashboard
- 🔧 **Gestión de Tarifas**: Modificación en línea de precios por hora
- 🔍 **Sistema de Búsqueda**: Consulta de vehículos y estados
- 💾 **Persistencia de Datos**: Almacenamiento automático en JSON

## 🚀 Instalación y Ejecución

### Opción 1: Ejecución Directa (Recomendada)

```cmd
# 1. Abrir CMD o PowerShell
# 2. Navegar al directorio
cd "c:\Users\usuario1\Documents\PROY-ESTACIONAMIENTO-PY"

# 3. Activar entorno virtual
.venv\Scripts\activate

# 4. Ejecutar aplicación
.venv\Scripts\python.exe app.py
```

### Opción 2: Validación Previa

```cmd
# Ejecutar validador del sistema
.venv\Scripts\python.exe validar_sistema.py
```

### 🌐 Acceso Web

- **Local**: http://localhost:8080
- **Red Local**: http://192.168.100.5:8080
- **Alternativo**: http://127.0.0.1:8080

## 🎯 Funcionalidades Detalladas

### 📊 Dashboard Principal
- Vista en tiempo real del estado del estacionamiento
- Estadísticas de ocupación y disponibilidad
- Tabla de vehículos actuales con acciones rápidas
- Botones de egreso individual por vehículo
- Actualización automática cada 30 segundos

### 🚗 Gestión de Vehículos
- **Ingreso**: Registro con placa, tipo y propietario opcional
- **Egreso**: Cálculo automático de tarifas por tiempo
- **Consulta**: Búsqueda por placa con información detallada
- **Validación**: Formato de placas colombianas flexible

### 🎫 Sistema de Abonos
- **Registro**: Abonos mensuales por tipo de vehículo
- **Descuentos**: 10% automático en cada uso
- **Gestión**: Renovación y cancelación de abonos
- **Calculadora**: Simulador de ahorros estimados

### 💰 Gestión de Tarifas
- **Edición en Línea**: Modificar precios sin recargar página
- **Validación**: Rangos entre $500 y $50,000 por hora
- **Simulador**: Calculadora de costos en tiempo real
- **Tipos**: Auto, Moto, Camión con tarifas diferenciadas

## 📋 Estructura del Proyecto

```
PROY-ESTACIONAMIENTO-PY/
├── 📄 app.py                    # Aplicación Flask principal
├── 📄 estacionamiento.py        # Lógica de negocio y clases
├── 📄 validar_sistema.py        # Script de validación
├── 📄 estacionamiento_datos.json # Persistencia de datos
├── 📁 templates/                # Plantillas HTML
│   ├── base.html               # Plantilla base
│   ├── index.html              # Dashboard principal
│   ├── ingresar.html           # Formulario de ingreso
│   ├── egresar.html            # Formulario de egreso  
│   ├── consultar.html          # Consulta de vehículos
│   ├── nuevo_abono.html        # Registro de abonos
│   ├── abonos.html             # Gestión de abonos
│   └── tarifas.html            # Configuración de tarifas
├── 📁 static/                   # Recursos estáticos
│   ├── css/style.css           # Estilos personalizados
│   └── js/main.js              # JavaScript personalizado  
├── 📁 .venv/                    # Entorno virtual Python
└── 📄 README.md                # Esta documentación
```

## 🔧 Tecnologías Utilizadas

- **Backend**: Python 3.13.5, Flask 3.1.2
- **Frontend**: HTML5, CSS3, JavaScript ES6
- **Framework CSS**: Bootstrap 5.1.3
- **Iconos**: Font Awesome 6.0.0
- **Persistencia**: JSON
- **Validación**: CSRF Protection, Form Validation

## 🛡️ Características de Seguridad

- ✅ **CSRF Protection**: Tokens en todos los formularios
- ✅ **Validación de Datos**: Servidor y cliente
- ✅ **Sanitización**: Entrada de datos segura
- ✅ **Formato de Placas**: Validación estricta
- ✅ **Rangos de Tarifas**: Límites configurables

## 📱 Compatibilidad

- **Navegadores**: Chrome, Firefox, Safari, Edge
- **Dispositivos**: PC, Tablet, Móvil
- **Sistemas**: Windows, macOS, Linux
- **Red**: Acceso local y por WiFi

## 🎉 Estado del Proyecto

✅ **COMPLETAMENTE FUNCIONAL**
- Todas las funcionalidades implementadas
- Interfaz web moderna y responsive  
- Validaciones de seguridad implementadas
- Sistema de persistencia funcionando
- Documentación completa

## 🚀 Para Desarrolladores

### Agregar Nuevas Funcionalidades
1. Modificar `estacionamiento.py` para lógica de negocio
2. Agregar rutas en `app.py`
3. Crear templates HTML en `templates/`
4. Ejecutar `validar_sistema.py` para verificar

### Comandos Útiles
```cmd
# Validar sistema completo
python validar_sistema.py

# Ejecutar en modo debug
python app.py

# Verificar dependencias
pip list

# Crear nuevo entorno virtual
python -m venv .venv
```

## 📞 Soporte

Para reportar problemas o solicitar nuevas funcionalidades, utilizar el sistema de issues del repositorio.

---

**Desarrollado con ❤️ en Python y Flask**

*Sistema de Estacionamiento v2.0 - Octubre 2025*