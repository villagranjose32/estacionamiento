"""
Aplicación Web del Sistema de Gestión de Estacionamiento
Usando Flask para crear una interfaz web
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from datetime import datetime
import json
import os

# Importar nuestras clases del sistema de estacionamiento
from estacionamiento import Estacionamiento, Vehiculo, AbonoMensual

app = Flask(__name__)
app.secret_key = 'estacionamiento_secret_key_2025'

# Instancia global del estacionamiento
estacionamiento = Estacionamiento(capacidad_total=50, nombre="Estacionamiento Web")

@app.route('/')
def index():
    """Página principal con el dashboard"""
    estado = {
        'nombre': estacionamiento.nombre,
        'capacidad_total': estacionamiento.capacidad_total,
        'ocupados': len(estacionamiento.vehiculos_actuales),
        'disponibles': estacionamiento.espacios_disponibles(),
        'porcentaje_ocupacion': (len(estacionamiento.vehiculos_actuales) / estacionamiento.capacidad_total) * 100,
        'vehiculos_actuales': list(estacionamiento.vehiculos_actuales.values()),
        'tarifas': estacionamiento.tarifas,
        'estadisticas_abonos': estacionamiento.obtener_estadisticas_abonos()
    }
    return render_template('index.html', estado=estado)

@app.route('/ingresar', methods=['GET', 'POST'])
def ingresar_vehiculo():
    """Formulario para ingresar vehículos"""
    if request.method == 'POST':
        placa = request.form.get('placa', '').strip()
        tipo_vehiculo = request.form.get('tipo_vehiculo', '').strip()
        propietario = request.form.get('propietario', '').strip()
        
        exito, mensaje, espacio = estacionamiento.registrar_ingreso(placa, tipo_vehiculo, propietario)
        
        if exito:
            flash(f'✅ {mensaje}', 'success')
        else:
            flash(f'❌ {mensaje}', 'error')
        
        return redirect(url_for('index'))
    
    return render_template('ingresar.html', tarifas=estacionamiento.tarifas)

@app.route('/egresar', methods=['GET', 'POST'])
def egresar_vehiculo():
    """Formulario para egresar vehículos"""
    if request.method == 'POST':
        placa = request.form.get('placa', '').strip()
        
        exito, mensaje, tarifa = estacionamiento.registrar_egreso(placa)
        
        if exito:
            flash(f'✅ {mensaje}', 'success')
        else:
            flash(f'❌ {mensaje}', 'error')
        
        return redirect(url_for('index'))
    
    # Obtener lista de vehículos actuales para el formulario
    vehiculos_actuales = list(estacionamiento.vehiculos_actuales.values())
    return render_template('egresar.html', vehiculos=vehiculos_actuales)

@app.route('/egresar-rapido', methods=['POST'])
def egresar_rapido():
    """Egreso rápido desde el dashboard"""
    try:
        data = request.get_json()
        placa = data.get('placa', '').strip()
        
        if not placa:
            return jsonify({
                'success': False,
                'message': 'Placa es requerida'
            }), 400
        
        # Verificar que el vehículo existe
        if placa not in estacionamiento.vehiculos_actuales:
            return jsonify({
                'success': False,
                'message': f'Vehículo {placa} no encontrado en el estacionamiento'
            }), 404
        
        # Obtener información del vehículo antes del egreso
        vehiculo = estacionamiento.vehiculos_actuales[placa]
        tiempo_permanencia = vehiculo.calcular_tiempo_permanencia()
        tarifa_calculada = estacionamiento.calcular_tarifa(vehiculo)
        
        # Procesar egreso
        exito, mensaje, tarifa = estacionamiento.registrar_egreso(placa)
        
        if exito:
            horas = int(tiempo_permanencia.total_seconds() // 3600)
            minutos = int((tiempo_permanencia.total_seconds() % 3600) // 60)
            
            return jsonify({
                'success': True,
                'message': 'Vehículo egresado exitosamente',
                'data': {
                    'placa': placa,
                    'tiempo_permanencia': f'{horas}h {minutos}m',
                    'tarifa': tarifa,
                    'tarifa_formateada': f'${tarifa:,.0f}',
                    'tipo_vehiculo': vehiculo.tipo_vehiculo,
                    'propietario': vehiculo.propietario or 'No especificado'
                }
            })
        else:
            return jsonify({
                'success': False,
                'message': mensaje
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error interno: {str(e)}'
        }), 500

@app.route('/consultar', methods=['GET', 'POST'])
def consultar_vehiculo():
    """Consultar información de un vehículo"""
    vehiculo_info = None
    
    if request.method == 'POST':
        placa = request.form.get('placa', '').strip()
        
        if placa:
            exito, mensaje = estacionamiento.consultar_vehiculo(placa)
            if exito:
                vehiculo = estacionamiento.vehiculos_actuales.get(placa.upper())
                if vehiculo:
                    tiempo_actual = vehiculo.calcular_tiempo_permanencia()
                    tarifa_actual = estacionamiento.calcular_tarifa(vehiculo)
                    
                    vehiculo_info = {
                        'vehiculo': vehiculo,
                        'tiempo_horas': int(tiempo_actual.total_seconds() // 3600),
                        'tiempo_minutos': int((tiempo_actual.total_seconds() % 3600) // 60),
                        'tarifa_actual': tarifa_actual,
                        'mensaje': mensaje
                    }
                flash('✅ Vehículo encontrado', 'success')
            else:
                flash(f'❌ {mensaje}', 'error')
    
    return render_template('consultar.html', vehiculo_info=vehiculo_info)

@app.route('/historial')
def ver_historial():
    """Ver el historial de vehículos"""
    # Obtener los últimos 20 registros del historial
    historial_reciente = estacionamiento.historial[-20:] if estacionamiento.historial else []
    
    # Calcular total recaudado
    total_recaudado = sum(v.tarifa_pagada for v in estacionamiento.historial)
    
    return render_template('historial.html', 
                         historial=historial_reciente, 
                         total_recaudado=total_recaudado,
                         total_registros=len(estacionamiento.historial))

@app.route('/tarifas', methods=['GET', 'POST'])
def gestionar_tarifas():
    """Gestionar las tarifas del estacionamiento"""
    if request.method == 'POST':
        nuevas_tarifas = {}
        
        for tipo in estacionamiento.tarifas.keys():
            nueva_tarifa = request.form.get(f'tarifa_{tipo}')
            if nueva_tarifa and nueva_tarifa.isdigit():
                nuevas_tarifas[tipo] = int(nueva_tarifa)
        
        if nuevas_tarifas:
            estacionamiento.cambiar_tarifas(nuevas_tarifas)
            flash('✅ Tarifas actualizadas correctamente', 'success')
        else:
            flash('❌ Error: Ingrese valores válidos para las tarifas', 'error')
        
        return redirect(url_for('gestionar_tarifas'))
    
    return render_template('tarifas.html', tarifas=estacionamiento.tarifas)

@app.route('/tarifas/modificar', methods=['POST'])
def modificar_tarifa():
    """Modificar una tarifa específica"""
    try:
        tipo_vehiculo = request.form.get('tipo_vehiculo')
        nueva_tarifa = request.form.get('nueva_tarifa')
        
        if not tipo_vehiculo or not nueva_tarifa:
            return jsonify({
                'success': False, 
                'message': 'Tipo de vehículo y tarifa son obligatorios'
            }), 400
        
        # Validar que sea un número entero positivo
        try:
            tarifa_int = int(nueva_tarifa)
            if tarifa_int <= 0:
                return jsonify({
                    'success': False, 
                    'message': 'La tarifa debe ser un número positivo'
                }), 400
        except ValueError:
            return jsonify({
                'success': False, 
                'message': 'La tarifa debe ser un número válido'
            }), 400
        
        # Validar que el tipo de vehículo exista
        if tipo_vehiculo not in estacionamiento.tarifas:
            return jsonify({
                'success': False, 
                'message': 'Tipo de vehículo no válido'
            }), 400
        
        # Validar rango razonable (entre 500 y 50000 pesos por hora)
        if tarifa_int < 500 or tarifa_int > 50000:
            return jsonify({
                'success': False, 
                'message': 'La tarifa debe estar entre $500 y $50.000 por hora'
            }), 400
        
        # Actualizar la tarifa
        tarifa_anterior = estacionamiento.tarifas[tipo_vehiculo]
        estacionamiento.cambiar_tarifas({tipo_vehiculo: tarifa_int})
        
        return jsonify({
            'success': True, 
            'message': f'Tarifa para {tipo_vehiculo} actualizada de ${tarifa_anterior:,} a ${tarifa_int:,}',
            'nueva_tarifa': tarifa_int,
            'tipo_vehiculo': tipo_vehiculo
        })
        
    except Exception as e:
        return jsonify({
            'success': False, 
            'message': f'Error interno: {str(e)}'
        }), 500

@app.route('/abonos')
def gestionar_abonos():
    """Ver todos los abonos mensuales"""
    abonos = estacionamiento.listar_abonos()
    estadisticas = estacionamiento.obtener_estadisticas_abonos()
    
    return render_template('abonos.html', 
                         abonos=abonos, 
                         estadisticas=estadisticas)

@app.route('/abonos/nuevo', methods=['GET', 'POST'])
def nuevo_abono():
    """Registrar un nuevo abono mensual"""
    if request.method == 'POST':
        placa = request.form.get('placa', '').strip()
        propietario = request.form.get('propietario', '').strip()
        tipo_vehiculo = request.form.get('tipo_vehiculo', '').strip()
        telefono = request.form.get('telefono', '').strip()
        email = request.form.get('email', '').strip()
        
        exito, mensaje, abono = estacionamiento.registrar_abono_mensual(
            placa, propietario, tipo_vehiculo, telefono, email
        )
        
        if exito:
            flash(f'✅ {mensaje}', 'success')
            return redirect(url_for('gestionar_abonos'))
        else:
            flash(f'❌ {mensaje}', 'error')
    
    costos_abonos = estacionamiento.obtener_costos_abonos_por_tipo()
    return render_template('nuevo_abono.html', 
                         costos_abonos=costos_abonos,
                         tarifas=estacionamiento.tarifas)

@app.route('/abonos/consultar', methods=['GET', 'POST'])
def consultar_abono():
    """Consultar el estado de un abono mensual"""
    abono_info = None
    
    if request.method == 'POST':
        placa = request.form.get('placa', '').strip()
        
        if placa:
            abono = estacionamiento.obtener_abono(placa)
            if abono:
                abono_info = {
                    'abono': abono,
                    'vigente': abono.esta_vigente(),
                    'dias_restantes': abono.dias_restantes(),
                    'puede_renovar': not abono.esta_vigente() or abono.dias_restantes() <= 7
                }
                flash('✅ Abono encontrado', 'success')
            else:
                flash(f'❌ No se encontró un abono para la placa {placa}', 'error')
    
    return render_template('consultar_abono.html', abono_info=abono_info)

@app.route('/abonos/renovar/<placa>', methods=['POST'])
def renovar_abono(placa):
    """Renovar un abono mensual"""
    exito, mensaje = estacionamiento.renovar_abono(placa)
    
    if exito:
        flash(f'✅ {mensaje}', 'success')
    else:
        flash(f'❌ {mensaje}', 'error')
    
    return redirect(url_for('gestionar_abonos'))

@app.route('/abonos/cancelar/<placa>', methods=['POST'])
def cancelar_abono(placa):
    """Cancelar un abono mensual"""
    exito, mensaje = estacionamiento.cancelar_abono(placa)
    
    if exito:
        flash(f'✅ {mensaje}', 'success')
    else:
        flash(f'❌ {mensaje}', 'error')
    
    return redirect(url_for('gestionar_abonos'))

# API endpoints para funcionalidad AJAX
@app.route('/api/estado')
def api_estado():
    """API para obtener el estado actual del estacionamiento"""
    return jsonify({
        'ocupados': len(estacionamiento.vehiculos_actuales),
        'disponibles': estacionamiento.espacios_disponibles(),
        'porcentaje_ocupacion': (len(estacionamiento.vehiculos_actuales) / estacionamiento.capacidad_total) * 100,
        'vehiculos_count': len(estacionamiento.vehiculos_actuales)
    })

@app.route('/api/vehiculos')
def api_vehiculos():
    """API para obtener la lista de vehículos actuales"""
    vehiculos_data = []
    for vehiculo in estacionamiento.vehiculos_actuales.values():
        tiempo = vehiculo.calcular_tiempo_permanencia()
        tarifa = estacionamiento.calcular_tarifa(vehiculo)
        
        tiene_abono = estacionamiento.tiene_abono_vigente(vehiculo.placa)
        
        vehiculos_data.append({
            'placa': vehiculo.placa,
            'tipo': vehiculo.tipo_vehiculo.capitalize(),
            'propietario': vehiculo.propietario,
            'espacio': vehiculo.espacio_asignado,
            'hora_entrada': vehiculo.hora_entrada.strftime('%H:%M:%S') if vehiculo.hora_entrada else '',
            'tiempo_horas': int(tiempo.total_seconds() // 3600),
            'tiempo_minutos': int((tiempo.total_seconds() % 3600) // 60),
            'tiene_abono': tiene_abono,
            'tarifa_actual': tarifa
        })
    
    return jsonify(vehiculos_data)

@app.route('/api/abonos')
def api_abonos():
    """API para obtener estadísticas de abonos"""
    estadisticas = estacionamiento.obtener_estadisticas_abonos()
    return jsonify(estadisticas)

@app.template_filter('currency')
def currency_filter(amount):
    """Filtro para formatear moneda"""
    return f"${amount:,.0f}"

if __name__ == '__main__':
    print("🚗 Iniciando Servidor Web del Sistema de Estacionamiento...")
    print("📍 Accede al sistema en: http://localhost:8080")
    print("📍 Acceso desde red: http://192.168.100.5:8080")
    print("⚠️  Para detener el servidor presiona Ctrl+C")
    
    app.run(debug=True, host='0.0.0.0', port=8080)