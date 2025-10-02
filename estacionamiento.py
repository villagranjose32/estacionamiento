"""
Sistema de Gestión de Estacionamiento
Autor: Sistema de IA
Fecha: 30 de septiembre de 2025

Este sistema permite gestionar el ingreso y egreso de vehículos en un estacionamiento,
incluyendo el cálculo de tarifas y el control de espacios disponibles.
"""

from datetime import datetime, timedelta
import json
import os

class Vehiculo:
    """Clase que representa un vehículo en el estacionamiento"""
    
    def __init__(self, placa, tipo_vehiculo, propietario=""):
        """
        Inicializa un nuevo vehículo
        
        Args:
            placa (str): Número de placa del vehículo
            tipo_vehiculo (str): Tipo de vehículo ('auto', 'moto', 'camioneta')
            propietario (str): Nombre del propietario (opcional)
        """
        self.placa = placa.upper()
        self.tipo_vehiculo = tipo_vehiculo.lower()
        self.propietario = propietario
        self.hora_entrada = None
        self.hora_salida = None
        self.espacio_asignado = None
        self.tarifa_pagada = 0.0
    
    def ingresar(self, espacio):
        """Registra el ingreso del vehículo al estacionamiento"""
        self.hora_entrada = datetime.now()
        self.espacio_asignado = espacio
    
    def egresar(self):
        """Registra el egreso del vehículo del estacionamiento"""
        self.hora_salida = datetime.now()
    
    def calcular_tiempo_permanencia(self):
        """Calcula el tiempo que el vehículo ha permanecido en el estacionamiento"""
        if self.hora_entrada:
            hora_calculo = self.hora_salida if self.hora_salida else datetime.now()
            return hora_calculo - self.hora_entrada
        return timedelta(0)
    
    def __str__(self):
        estado = "Dentro" if self.hora_salida is None else "Salió"
        tiempo = self.calcular_tiempo_permanencia()
        horas = int(tiempo.total_seconds() // 3600)
        minutos = int((tiempo.total_seconds() % 3600) // 60)
        
        return f"Placa: {self.placa} | Tipo: {self.tipo_vehiculo.capitalize()} | " \
               f"Espacio: {self.espacio_asignado} | Estado: {estado} | " \
               f"Tiempo: {horas}h {minutos}m"


class AbonoMensual:
    """Clase que representa un abono mensual para un vehículo"""
    
    def __init__(self, placa, propietario, tipo_vehiculo="auto", telefono="", email=""):
        """
        Inicializa un nuevo abono mensual
        
        Args:
            placa (str): Número de placa del vehículo
            propietario (str): Nombre del propietario
            tipo_vehiculo (str): Tipo de vehículo (moto, auto, camioneta)
            telefono (str): Teléfono del propietario
            email (str): Email del propietario
        """
        self.placa = placa.upper()
        self.propietario = propietario
        self.tipo_vehiculo = tipo_vehiculo.lower()
        self.telefono = telefono
        self.email = email
        self.fecha_inicio = datetime.now()
        self.fecha_vencimiento = self.fecha_inicio + timedelta(days=30)
        self.activo = True
        self.monto_pagado = 0
        self.descuento_aplicado = 10  # 10% de descuento
    
    def esta_vigente(self):
        """Verifica si el abono está vigente"""
        return self.activo and datetime.now() <= self.fecha_vencimiento
    
    def dias_restantes(self):
        """Calcula los días restantes del abono"""
        if not self.esta_vigente():
            return 0
        
        diferencia = self.fecha_vencimiento - datetime.now()
        return max(0, diferencia.days)
    
    def renovar(self):
        """Renueva el abono por 30 días más"""
        self.fecha_inicio = datetime.now()
        self.fecha_vencimiento = self.fecha_inicio + timedelta(days=30)
        self.activo = True
    
    def cancelar(self):
        """Cancela el abono mensual"""
        self.activo = False
    
    def __str__(self):
        estado = "Vigente" if self.esta_vigente() else "Vencido"
        dias = self.dias_restantes()
        return f"Placa: {self.placa} | Tipo: {self.tipo_vehiculo.capitalize()} | " \
               f"Propietario: {self.propietario} | Estado: {estado} | Días restantes: {dias}"


class Estacionamiento:
    """Clase principal que gestiona el estacionamiento"""
    
    def __init__(self, capacidad_total=50, nombre="Estacionamiento Principal"):
        """
        Inicializa el estacionamiento
        
        Args:
            capacidad_total (int): Número máximo de espacios
            nombre (str): Nombre del estacionamiento
        """
        self.nombre = nombre
        self.capacidad_total = capacidad_total
        self.vehiculos_actuales = {}  # placa -> Vehiculo
        self.historial = []  # Lista de todos los vehículos que han pasado
        self.espacios_ocupados = set()
        self.abonos_mensuales = {}  # placa -> AbonoMensual
        
        # Tarifas por hora según el tipo de vehículo
        self.tarifas = {
            'moto': 1500,      # $1500 por hora
            'auto': 2500,      # $2500 por hora
            'camioneta': 3500  # $3500 por hora
        }
        
        # Archivo para persistir datos
        self.archivo_datos = "estacionamiento_datos.json"
        self.cargar_datos()
    
    def espacios_disponibles(self):
        """Retorna el número de espacios disponibles"""
        return self.capacidad_total - len(self.vehiculos_actuales)
    
    def asignar_espacio(self):
        """Asigna un espacio disponible"""
        for i in range(1, self.capacidad_total + 1):
            if i not in self.espacios_ocupados:
                return i
        return None
    
    def calcular_tarifa(self, vehiculo):
        """
        Calcula la tarifa a pagar por un vehículo
        
        Args:
            vehiculo (Vehiculo): El vehículo para calcular la tarifa
            
        Returns:
            float: Monto a pagar
        """
        tiempo_permanencia = vehiculo.calcular_tiempo_permanencia()
        horas = tiempo_permanencia.total_seconds() / 3600
        
        # Se cobra mínimo 1 hora, y se redondea hacia arriba
        horas_a_cobrar = max(1, int(horas) + (1 if horas % 1 > 0 else 0))
        
        tarifa_por_hora = self.tarifas.get(vehiculo.tipo_vehiculo, self.tarifas['auto'])
        tarifa_base = horas_a_cobrar * tarifa_por_hora
        
        # Aplicar descuento si el vehículo tiene abono mensual vigente
        if self.tiene_abono_vigente(vehiculo.placa):
            descuento = tarifa_base * 0.10  # 10% de descuento
            return tarifa_base - descuento
        
        return tarifa_base
    
    def registrar_ingreso(self, placa, tipo_vehiculo, propietario=""):
        """
        Registra el ingreso de un vehículo al estacionamiento
        
        Args:
            placa (str): Placa del vehículo
            tipo_vehiculo (str): Tipo de vehículo
            propietario (str): Propietario del vehículo
            
        Returns:
            tuple: (éxito, mensaje, espacio_asignado)
        """
        placa = placa.upper().strip()
        
        # Validaciones
        if not placa:
            return False, "La placa no puede estar vacía", None
        
        if placa in self.vehiculos_actuales:
            return False, f"El vehículo con placa {placa} ya está en el estacionamiento", None
        
        if len(self.vehiculos_actuales) >= self.capacidad_total:
            return False, "El estacionamiento está lleno", None
        
        if tipo_vehiculo.lower() not in self.tarifas:
            return False, f"Tipo de vehículo no válido. Tipos permitidos: {list(self.tarifas.keys())}", None
        
        # Crear el vehículo y asignar espacio
        vehiculo = Vehiculo(placa, tipo_vehiculo, propietario)
        espacio = self.asignar_espacio()
        
        if espacio is None:
            return False, "No hay espacios disponibles", None
        
        # Registrar ingreso
        vehiculo.ingresar(espacio)
        self.vehiculos_actuales[placa] = vehiculo
        self.espacios_ocupados.add(espacio)
        
        # Guardar datos
        self.guardar_datos()
        
        return True, f"Vehículo ingresado exitosamente en el espacio {espacio}", espacio
    
    def registrar_egreso(self, placa):
        """
        Registra el egreso de un vehículo del estacionamiento
        
        Args:
            placa (str): Placa del vehículo a dar salida
            
        Returns:
            tuple: (éxito, mensaje, tarifa_a_pagar)
        """
        placa = placa.upper().strip()
        
        if not placa:
            return False, "La placa no puede estar vacía", 0
        
        if placa not in self.vehiculos_actuales:
            return False, f"El vehículo con placa {placa} no se encuentra en el estacionamiento", 0
        
        # Obtener el vehículo y calcular tarifa
        vehiculo = self.vehiculos_actuales[placa]
        tarifa = self.calcular_tarifa(vehiculo)
        
        # Registrar egreso
        vehiculo.egresar()
        vehiculo.tarifa_pagada = tarifa
        
        # Liberar espacio
        if vehiculo.espacio_asignado:
            self.espacios_ocupados.discard(vehiculo.espacio_asignado)
        
        # Mover al historial y quitar de vehículos actuales
        self.historial.append(vehiculo)
        del self.vehiculos_actuales[placa]
        
        # Guardar datos
        self.guardar_datos()
        
        tiempo = vehiculo.calcular_tiempo_permanencia()
        horas = int(tiempo.total_seconds() // 3600)
        minutos = int((tiempo.total_seconds() % 3600) // 60)
        
        mensaje = f"Vehículo {placa} salió del estacionamiento.\n"
        mensaje += f"Tiempo de permanencia: {horas}h {minutos}m\n"
        mensaje += f"Tarifa a pagar: ${tarifa:,.0f}"
        
        return True, mensaje, tarifa
    
    def consultar_vehiculo(self, placa):
        """Consulta el estado de un vehículo en el estacionamiento"""
        placa = placa.upper().strip()
        
        if placa in self.vehiculos_actuales:
            vehiculo = self.vehiculos_actuales[placa]
            tiempo_actual = vehiculo.calcular_tiempo_permanencia()
            tarifa_actual = self.calcular_tarifa(vehiculo)
            
            horas = int(tiempo_actual.total_seconds() // 3600)
            minutos = int((tiempo_actual.total_seconds() % 3600) // 60)
            
            info = f"Vehículo encontrado:\n"
            info += f"Placa: {vehiculo.placa}\n"
            info += f"Tipo: {vehiculo.tipo_vehiculo.capitalize()}\n"
            info += f"Propietario: {vehiculo.propietario if vehiculo.propietario else 'No especificado'}\n"
            info += f"Espacio: {vehiculo.espacio_asignado}\n"
            info += f"Hora de entrada: {vehiculo.hora_entrada.strftime('%d/%m/%Y %H:%M:%S')}\n"
            info += f"Tiempo transcurrido: {horas}h {minutos}m\n"
            info += f"Tarifa actual: ${tarifa_actual:,.0f}"
            
            return True, info
        else:
            return False, f"El vehículo con placa {placa} no se encuentra en el estacionamiento"
    
    def obtener_estado_general(self):
        """Obtiene el estado general del estacionamiento"""
        ocupados = len(self.vehiculos_actuales)
        disponibles = self.espacios_disponibles()
        porcentaje_ocupacion = (ocupados / self.capacidad_total) * 100
        
        estado = f"=== ESTADO DEL ESTACIONAMIENTO ===\n"
        estado += f"Nombre: {self.nombre}\n"
        estado += f"Capacidad total: {self.capacidad_total} espacios\n"
        estado += f"Espacios ocupados: {ocupados}\n"
        estado += f"Espacios disponibles: {disponibles}\n"
        estado += f"Ocupación: {porcentaje_ocupacion:.1f}%\n"
        
        if self.vehiculos_actuales:
            estado += f"\n=== VEHÍCULOS ACTUALES ===\n"
            for vehiculo in self.vehiculos_actuales.values():
                estado += str(vehiculo) + "\n"
        
        return estado
    
    def cambiar_tarifas(self, nuevas_tarifas):
        """Permite modificar las tarifas del estacionamiento"""
        for tipo, tarifa in nuevas_tarifas.items():
            if tipo in self.tarifas:
                self.tarifas[tipo] = tarifa
        self.guardar_datos()
        return True, "Tarifas actualizadas correctamente"
    
    def guardar_datos(self):
        """Guarda los datos del estacionamiento en un archivo JSON"""
        try:
            datos = {
                'nombre': self.nombre,
                'capacidad_total': self.capacidad_total,
                'tarifas': self.tarifas,
                'vehiculos_actuales': {},
                'historial_resumido': [],
                'abonos_mensuales': {}
            }
            
            # Guardar vehículos actuales
            for placa, vehiculo in self.vehiculos_actuales.items():
                datos['vehiculos_actuales'][placa] = {
                    'placa': vehiculo.placa,
                    'tipo_vehiculo': vehiculo.tipo_vehiculo,
                    'propietario': vehiculo.propietario,
                    'hora_entrada': vehiculo.hora_entrada.isoformat() if vehiculo.hora_entrada else None,
                    'espacio_asignado': vehiculo.espacio_asignado
                }
            
            # Guardar resumen del historial (últimos 100 registros)
            for vehiculo in self.historial[-100:]:
                datos['historial_resumido'].append({
                    'placa': vehiculo.placa,
                    'tipo_vehiculo': vehiculo.tipo_vehiculo,
                    'hora_entrada': vehiculo.hora_entrada.isoformat() if vehiculo.hora_entrada else None,
                    'hora_salida': vehiculo.hora_salida.isoformat() if vehiculo.hora_salida else None,
                    'tarifa_pagada': vehiculo.tarifa_pagada
                })
            
            # Guardar abonos mensuales
            for placa, abono in self.abonos_mensuales.items():
                datos['abonos_mensuales'][placa] = {
                    'placa': abono.placa,
                    'propietario': abono.propietario,
                    'tipo_vehiculo': abono.tipo_vehiculo,
                    'telefono': abono.telefono,
                    'email': abono.email,
                    'fecha_inicio': abono.fecha_inicio.isoformat() if abono.fecha_inicio else None,
                    'fecha_vencimiento': abono.fecha_vencimiento.isoformat() if abono.fecha_vencimiento else None,
                    'activo': abono.activo,
                    'monto_pagado': abono.monto_pagado,
                    'descuento_aplicado': abono.descuento_aplicado
                }
            
            with open(self.archivo_datos, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Error al guardar datos: {e}")
    
    def cargar_datos(self):
        """Carga los datos del estacionamiento desde un archivo JSON"""
        try:
            if os.path.exists(self.archivo_datos):
                with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                
                # Restaurar configuración básica
                self.nombre = datos.get('nombre', self.nombre)
                self.capacidad_total = datos.get('capacidad_total', self.capacidad_total)
                self.tarifas = datos.get('tarifas', self.tarifas)
                
                # Restaurar vehículos actuales
                vehiculos_data = datos.get('vehiculos_actuales', {})
                for placa, datos_vehiculo in vehiculos_data.items():
                    vehiculo = Vehiculo(
                        datos_vehiculo['placa'],
                        datos_vehiculo['tipo_vehiculo'],
                        datos_vehiculo.get('propietario', '')
                    )
                    if datos_vehiculo.get('hora_entrada'):
                        vehiculo.hora_entrada = datetime.fromisoformat(datos_vehiculo['hora_entrada'])
                    vehiculo.espacio_asignado = datos_vehiculo.get('espacio_asignado')
                    
                    self.vehiculos_actuales[placa] = vehiculo
                    if vehiculo.espacio_asignado:
                        self.espacios_ocupados.add(vehiculo.espacio_asignado)
                
                # Restaurar historial resumido
                historial_data = datos.get('historial_resumido', [])
                for datos_vehiculo in historial_data:
                    vehiculo = Vehiculo(
                        datos_vehiculo['placa'],
                        datos_vehiculo['tipo_vehiculo']
                    )
                    if datos_vehiculo.get('hora_entrada'):
                        vehiculo.hora_entrada = datetime.fromisoformat(datos_vehiculo['hora_entrada'])
                    if datos_vehiculo.get('hora_salida'):
                        vehiculo.hora_salida = datetime.fromisoformat(datos_vehiculo['hora_salida'])
                    vehiculo.tarifa_pagada = datos_vehiculo.get('tarifa_pagada', 0)
                    
                    self.historial.append(vehiculo)
                
                # Restaurar abonos mensuales
                abonos_data = datos.get('abonos_mensuales', {})
                for placa, datos_abono in abonos_data.items():
                    abono = AbonoMensual(
                        datos_abono['placa'],
                        datos_abono['propietario'],
                        datos_abono.get('tipo_vehiculo', 'auto'),
                        datos_abono.get('telefono', ''),
                        datos_abono.get('email', '')
                    )
                    if datos_abono.get('fecha_inicio'):
                        abono.fecha_inicio = datetime.fromisoformat(datos_abono['fecha_inicio'])
                    if datos_abono.get('fecha_vencimiento'):
                        abono.fecha_vencimiento = datetime.fromisoformat(datos_abono['fecha_vencimiento'])
                    abono.activo = datos_abono.get('activo', True)
                    abono.monto_pagado = datos_abono.get('monto_pagado', 0)
                    abono.descuento_aplicado = datos_abono.get('descuento_aplicado', 10)
                    
                    self.abonos_mensuales[placa] = abono
                    
        except Exception as e:
            print(f"Error al cargar datos: {e}")
            print("Se iniciará con datos en blanco.")
    
    # Métodos para gestión de abonos mensuales
    def registrar_abono_mensual(self, placa, propietario, tipo_vehiculo="auto", telefono="", email=""):
        """
        Registra un nuevo abono mensual
        
        Args:
            placa (str): Placa del vehículo
            propietario (str): Nombre del propietario
            tipo_vehiculo (str): Tipo de vehículo (moto, auto, camioneta)
            telefono (str): Teléfono del propietario
            email (str): Email del propietario
            
        Returns:
            tuple: (éxito, mensaje, abono)
        """
        placa = placa.upper().strip()
        tipo_vehiculo = tipo_vehiculo.lower().strip()
        
        # Validaciones
        if not placa:
            return False, "La placa no puede estar vacía", None
        
        if not propietario.strip():
            return False, "El nombre del propietario es obligatorio", None
        
        if tipo_vehiculo not in self.tarifas:
            return False, f"Tipo de vehículo no válido. Tipos permitidos: {list(self.tarifas.keys())}", None
        
        if placa in self.abonos_mensuales and self.abonos_mensuales[placa].esta_vigente():
            return False, f"El vehículo {placa} ya tiene un abono mensual vigente", None
        
        # Crear el abono mensual
        abono = AbonoMensual(placa, propietario.strip(), tipo_vehiculo, telefono.strip(), email.strip())
        
        # Calcular costo del abono basado en el tipo de vehículo
        costo_abono = self.calcular_costo_abono_mensual(tipo_vehiculo)
        abono.monto_pagado = costo_abono
        
        self.abonos_mensuales[placa] = abono
        
        # Guardar datos
        self.guardar_datos()
        
        return True, f"Abono mensual registrado exitosamente para {placa} ({tipo_vehiculo}). Válido hasta {abono.fecha_vencimiento.strftime('%d/%m/%Y')}", abono
    
    def tiene_abono_vigente(self, placa):
        """Verifica si un vehículo tiene abono mensual vigente"""
        placa = placa.upper().strip()
        return placa in self.abonos_mensuales and self.abonos_mensuales[placa].esta_vigente()
    
    def obtener_abono(self, placa):
        """Obtiene el abono mensual de un vehículo"""
        placa = placa.upper().strip()
        return self.abonos_mensuales.get(placa)
    
    def renovar_abono(self, placa):
        """Renueva un abono mensual existente"""
        placa = placa.upper().strip()
        
        if placa not in self.abonos_mensuales:
            return False, f"No existe un abono registrado para el vehículo {placa}"
        
        abono = self.abonos_mensuales[placa]
        abono.renovar()
        
        # Calcular nuevo costo
        costo_renovacion = self.calcular_costo_abono_mensual()
        abono.monto_pagado = costo_renovacion
        
        # Guardar datos
        self.guardar_datos()
        
        return True, f"Abono renovado exitosamente. Válido hasta {abono.fecha_vencimiento.strftime('%d/%m/%Y')}"
    
    def cancelar_abono(self, placa):
        """Cancela un abono mensual"""
        placa = placa.upper().strip()
        
        if placa not in self.abonos_mensuales:
            return False, f"No existe un abono registrado para el vehículo {placa}"
        
        abono = self.abonos_mensuales[placa]
        abono.cancelar()
        
        # Guardar datos
        self.guardar_datos()
        
        return True, f"Abono cancelado para el vehículo {placa}"
    
    def listar_abonos(self, solo_vigentes=False):
        """Lista todos los abonos mensuales"""
        if solo_vigentes:
            return {placa: abono for placa, abono in self.abonos_mensuales.items() if abono.esta_vigente()}
        return self.abonos_mensuales
    
    def calcular_costo_abono_mensual(self, tipo_vehiculo="auto"):
        """
        Calcula el costo del abono mensual basado en el tipo de vehículo
        Estimación: 8 horas diarias x 22 días laborales = 176 horas mensuales
        Se aplica sobre la tarifa del tipo de vehículo específico
        
        Args:
            tipo_vehiculo (str): Tipo de vehículo para calcular el costo
        """
        horas_estimadas_mes = 176  # 8 horas x 22 días laborales
        tarifa_por_hora = self.tarifas.get(tipo_vehiculo, self.tarifas['auto'])
        costo_sin_descuento = horas_estimadas_mes * tarifa_por_hora
        descuento = costo_sin_descuento * 0.30  # 30% de descuento por abono mensual
        return int(costo_sin_descuento - descuento)
    
    def obtener_costos_abonos_por_tipo(self):
        """Obtiene los costos de abono para todos los tipos de vehículo"""
        costos = {}
        for tipo in self.tarifas.keys():
            costos[tipo] = self.calcular_costo_abono_mensual(tipo)
        return costos
    
    def obtener_estadisticas_abonos(self):
        """Obtiene estadísticas de los abonos mensuales"""
        total_abonos = len(self.abonos_mensuales)
        abonos_vigentes = len([a for a in self.abonos_mensuales.values() if a.esta_vigente()])
        abonos_vencidos = total_abonos - abonos_vigentes
        
        ingresos_abonos = sum(a.monto_pagado for a in self.abonos_mensuales.values() if a.esta_vigente())
        
        return {
            'total_abonos': total_abonos,
            'abonos_vigentes': abonos_vigentes,
            'abonos_vencidos': abonos_vencidos,
            'ingresos_mensuales': ingresos_abonos,
            'costo_abono': self.calcular_costo_abono_mensual()
        }


def mostrar_menu():
    """Muestra el menú principal del sistema"""
    print("\n" + "="*50)
    print("    SISTEMA DE GESTIÓN DE ESTACIONAMIENTO")
    print("="*50)
    print("1. Registrar ingreso de vehículo")
    print("2. Registrar egreso de vehículo") 
    print("3. Consultar vehículo")
    print("4. Ver estado del estacionamiento")
    print("5. Modificar tarifas")
    print("6. Ver historial de vehículos")
    print("7. Salir")
    print("="*50)


def validar_placa(placa):
    """Valida que la placa tenga un formato básico y flexible"""
    placa = placa.strip().upper()
    
    # Verificar longitud
    if len(placa) < 3 or len(placa) > 8:
        return False, "La placa debe tener entre 3 y 8 caracteres"
    
    # Limpiar y validar caracteres permitidos (letras, números y guiones)
    placa_limpia = placa.replace("-", "").replace(" ", "")
    if not placa_limpia.isalnum():
        return False, "La placa solo puede contener letras, números, guiones y espacios"
    
    # Verificar que tenga al menos una letra y un número (formato típico de placas)
    tiene_letra = any(c.isalpha() for c in placa_limpia)
    tiene_numero = any(c.isdigit() for c in placa_limpia)
    
    if not (tiene_letra and tiene_numero):
        return False, "La placa debe contener al menos una letra y un número"
    
    return True, placa


def main():
    """Función principal del programa"""
    print("Inicializando Sistema de Gestión de Estacionamiento...")
    
    # Crear instancia del estacionamiento
    estacionamiento = Estacionamiento()
    
    print(f"Sistema iniciado: {estacionamiento.nombre}")
    print(f"Capacidad: {estacionamiento.capacidad_total} espacios")
    
    while True:
        try:
            mostrar_menu()
            opcion = input("Seleccione una opción (1-7): ").strip()
            
            if opcion == "1":
                # Registrar ingreso
                print("\n--- REGISTRAR INGRESO DE VEHÍCULO ---")
                placa = input("Ingrese la placa del vehículo: ").strip()
                
                valida, resultado = validar_placa(placa)
                if not valida:
                    print(f"Error: {resultado}")
                    continue
                placa = resultado
                
                print("Tipos de vehículo disponibles:")
                for tipo, tarifa in estacionamiento.tarifas.items():
                    print(f"  - {tipo.capitalize()}: ${tarifa:,.0f} por hora")
                
                tipo_vehiculo = input("Ingrese el tipo de vehículo: ").strip().lower()
                propietario = input("Ingrese el nombre del propietario (opcional): ").strip()
                
                exito, mensaje, espacio = estacionamiento.registrar_ingreso(placa, tipo_vehiculo, propietario)
                
                if exito:
                    print(f"✅ {mensaje}")
                    print(f"Espacios disponibles: {estacionamiento.espacios_disponibles()}")
                else:
                    print(f"❌ Error: {mensaje}")
            
            elif opcion == "2":
                # Registrar egreso
                print("\n--- REGISTRAR EGRESO DE VEHÍCULO ---")
                placa = input("Ingrese la placa del vehículo: ").strip()
                
                exito, mensaje, tarifa = estacionamiento.registrar_egreso(placa)
                
                if exito:
                    print(f"✅ {mensaje}")
                    confirmacion = input("¿Confirmar pago? (s/n): ").strip().lower()
                    if confirmacion == 's':
                        print("💰 Pago registrado correctamente")
                    print(f"Espacios disponibles: {estacionamiento.espacios_disponibles()}")
                else:
                    print(f"❌ Error: {mensaje}")
            
            elif opcion == "3":
                # Consultar vehículo
                print("\n--- CONSULTAR VEHÍCULO ---")
                placa = input("Ingrese la placa del vehículo: ").strip()
                
                exito, mensaje = estacionamiento.consultar_vehiculo(placa)
                
                if exito:
                    print(f"📋 {mensaje}")
                else:
                    print(f"❌ {mensaje}")
            
            elif opcion == "4":
                # Ver estado del estacionamiento
                print("\n" + estacionamiento.obtener_estado_general())
            
            elif opcion == "5":
                # Modificar tarifas
                print("\n--- MODIFICAR TARIFAS ---")
                print("Tarifas actuales:")
                for tipo, tarifa in estacionamiento.tarifas.items():
                    print(f"  {tipo.capitalize()}: ${tarifa:,.0f} por hora")
                
                tipo_modificar = input("¿Qué tipo de vehículo desea modificar?: ").strip().lower()
                
                if tipo_modificar in estacionamiento.tarifas:
                    try:
                        nueva_tarifa = int(input(f"Ingrese la nueva tarifa para {tipo_modificar}: $"))
                        if nueva_tarifa > 0:
                            estacionamiento.cambiar_tarifas({tipo_modificar: nueva_tarifa})
                            print(f"✅ Tarifa para {tipo_modificar} actualizada a ${nueva_tarifa:,.0f}")
                        else:
                            print("❌ Error: La tarifa debe ser mayor a 0")
                    except ValueError:
                        print("❌ Error: Ingrese un número válido")
                else:
                    print(f"❌ Error: Tipo de vehículo '{tipo_modificar}' no válido")
            
            elif opcion == "6":
                # Ver historial
                print("\n--- HISTORIAL DE VEHÍCULOS ---")
                if estacionamiento.historial:
                    print(f"Últimos {len(estacionamiento.historial)} registros:")
                    total_recaudado = 0
                    for vehiculo in estacionamiento.historial[-10:]:  # Mostrar últimos 10
                        tiempo = vehiculo.calcular_tiempo_permanencia()
                        horas = int(tiempo.total_seconds() // 3600)
                        minutos = int((tiempo.total_seconds() % 3600) // 60)
                        print(f"  {vehiculo.placa} | {vehiculo.tipo_vehiculo.capitalize()} | "
                              f"{horas}h {minutos}m | ${vehiculo.tarifa_pagada:,.0f}")
                        total_recaudado += vehiculo.tarifa_pagada
                    
                    print(f"\nTotal recaudado (últimos registros): ${total_recaudado:,.0f}")
                else:
                    print("No hay registros en el historial")
            
            elif opcion == "7":
                # Salir
                print("\n¡Gracias por usar el Sistema de Gestión de Estacionamiento!")
                print("Los datos han sido guardados automáticamente.")
                break
            
            else:
                print("❌ Opción no válida. Por favor seleccione una opción del 1 al 7.")
        
        except KeyboardInterrupt:
            print("\n\nSaliendo del sistema...")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            print("El sistema continuará funcionando...")


if __name__ == "__main__":
    main()
