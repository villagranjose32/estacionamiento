# Sistema de Gestión de Estacionamiento

Este es un sistema completo para gestionar el ingreso y egreso de vehículos en un estacionamiento, desarrollado en Python.

## Características Principales

### 🚗 Gestión de Vehículos
- Registro de ingreso con asignación automática de espacios
- Registro de egreso con cálculo automático de tarifas
- Consulta de estado de vehículos en tiempo real
- Validación de placas y tipos de vehículos

### 💰 Sistema de Tarifas
- Tarifas diferenciadas por tipo de vehículo:
  - **Motos**: $1,500 por hora
  - **Autos**: $2,500 por hora  
  - **Camionetas**: $3,500 por hora
- Cálculo automático basado en tiempo de permanencia
- Tarifas modificables desde el sistema

### 📊 Reportes y Estadísticas
- Estado general del estacionamiento en tiempo real
- Porcentaje de ocupación
- Historial completo de vehículos
- Total de ingresos generados

### 💾 Persistencia de Datos
- Almacenamiento automático en archivo JSON
- Recuperación de datos al reiniciar el sistema
- Respaldo del historial de transacciones

## Estructura del Sistema

### Clases Principales

#### `Vehiculo`
Representa un vehículo individual con sus propiedades:
- Placa, tipo de vehículo, propietario
- Horas de entrada y salida
- Espacio asignado
- Tarifa pagada

#### `Estacionamiento`
Clase principal que gestiona todo el estacionamiento:
- Control de capacidad y espacios disponibles
- Registro de ingresos y egresos
- Cálculo de tarifas
- Persistencia de datos

## Instalación y Uso

### Requisitos
- Python 3.6 o superior
- No requiere librerías externas (solo bibliotecas estándar)

### Ejecución
1. Abrir terminal en la carpeta del proyecto
2. Ejecutar el comando:
   ```bash
   python estacionamiento.py
   ```

### Menú Principal
El sistema presenta un menú interactivo con las siguientes opciones:

1. **Registrar ingreso de vehículo**
   - Ingresa la placa del vehículo
   - Selecciona el tipo de vehículo
   - Opcionalmente ingresa el nombre del propietario
   - El sistema asigna automáticamente un espacio

2. **Registrar egreso de vehículo**
   - Ingresa la placa del vehículo
   - El sistema calcula automáticamente el tiempo y la tarifa
   - Confirma el pago

3. **Consultar vehículo**
   - Busca un vehículo por su placa
   - Muestra información detallada y tarifa actual

4. **Ver estado del estacionamiento**
   - Muestra ocupación actual
   - Lista todos los vehículos presentes
   - Estadísticas generales

5. **Modificar tarifas**
   - Permite cambiar las tarifas por tipo de vehículo
   - Los cambios se guardan automáticamente

6. **Ver historial de vehículos**
   - Muestra los últimos registros
   - Total recaudado

7. **Salir**
   - Cierra el sistema guardando todos los datos

## Configuración

### Capacidad del Estacionamiento
Por defecto, el estacionamiento tiene capacidad para 50 vehículos. Esto se puede modificar en el constructor de la clase `Estacionamiento`.

### Archivo de Datos
Los datos se almacenan en `estacionamiento_datos.json` en el mismo directorio del programa.

## Validaciones Incluidas

- **Placa**: Entre 3 y 8 caracteres, solo letras, números y guiones
- **Tipo de vehículo**: Solo acepta tipos válidos (moto, auto, camioneta)
- **Capacidad**: No permite ingresos si el estacionamiento está lleno
- **Vehículos duplicados**: No permite el mismo vehículo dos veces

## Ejemplos de Uso

### Registrar un Auto
```
Placa: ABC123
Tipo: auto
Propietario: Juan Pérez
```

### Consultar Tarifa
Al consultar un vehículo que lleva 2 horas y 30 minutos:
- Se cobrarán 3 horas completas (redondeo hacia arriba)
- Auto: 3 × $2,500 = $7,500

## Personalización

El sistema es fácilmente personalizable:

- **Tarifas**: Modifica el diccionario `self.tarifas` en la clase `Estacionamiento`
- **Capacidad**: Cambia el parámetro `capacidad_total` 
- **Tipos de vehículo**: Agrega nuevos tipos al diccionario de tarifas
- **Archivo de datos**: Modifica `self.archivo_datos`

## Características Técnicas

- **Orientado a objetos**: Código organizado en clases reutilizables
- **Manejo de errores**: Validaciones y excepciones controladas
- **Persistencia**: Almacenamiento automático de datos
- **Interfaz amigable**: Menú intuitivo con emojis y colores
- **Código documentado**: Docstrings en todas las funciones

## Posibles Mejoras Futuras

- Interfaz gráfica con tkinter o PyQt
- Base de datos SQL para mejor rendimiento
- Sistema de reservas
- Notificaciones automáticas
- Integración con sistemas de pago
- Reportes en PDF o Excel
- API REST para integración con otros sistemas

---

**Desarrollado con Python 3** | **Fecha: 30 de septiembre de 2025**