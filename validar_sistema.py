#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para validar la configuración y estructura del sistema de estacionamiento
"""

import os
import json
import sys
from pathlib import Path

def validar_estructura_archivos():
    """Valida que todos los archivos necesarios estén presentes"""
    print("🔍 Validando estructura de archivos...")
    
    archivos_requeridos = [
        'app.py',
        'estacionamiento.py',
        'templates/base.html',
        'templates/index.html',
        'templates/ingresar.html',
        'templates/egresar.html',
        'templates/consultar.html',
        'templates/nuevo_abono.html',
        'templates/tarifas.html',
        'templates/abonos.html',
        'static/css/style.css',
        'static/js/main.js'
    ]
    
    archivos_faltantes = []
    
    for archivo in archivos_requeridos:
        if not os.path.exists(archivo):
            archivos_faltantes.append(archivo)
        else:
            print(f"  ✅ {archivo}")
    
    if archivos_faltantes:
        print(f"  ❌ Archivos faltantes: {', '.join(archivos_faltantes)}")
        return False
    
    return True

def validar_datos_json():
    """Valida el archivo de datos JSON"""
    print("\n📊 Validando archivo de datos...")
    
    if os.path.exists('estacionamiento_datos.json'):
        try:
            with open('estacionamiento_datos.json', 'r', encoding='utf-8') as f:
                datos = json.load(f)
            print("  ✅ Archivo JSON válido")
            print(f"  📈 Vehículos actuales: {len(datos.get('vehiculos_actuales', {}))}")
            print(f"  📋 Historial: {len(datos.get('historial', []))}")
            print(f"  🎫 Abonos: {len(datos.get('abonos_mensuales', {}))}")
            return True
        except json.JSONDecodeError as e:
            print(f"  ❌ Error en JSON: {e}")
            return False
    else:
        print("  ⚠️  Archivo de datos no existe (se creará automáticamente)")
        return True

def validar_imports():
    """Valida que se puedan importar los módulos necesarios"""
    print("\n📦 Validando dependencias...")
    
    try:
        import flask
        print(f"  ✅ Flask {flask.__version__}")
    except ImportError:
        print("  ❌ Flask no está instalado")
        return False
    
    try:
        from estacionamiento import Estacionamiento
        print("  ✅ Módulo estacionamiento.py")
    except ImportError as e:
        print(f"  ❌ Error importando estacionamiento.py: {e}")
        return False
    
    return True

def validar_configuracion_app():
    """Valida la configuración de la aplicación Flask"""
    print("\n⚙️  Validando configuración de la aplicación...")
    
    try:
        # Importar sin ejecutar
        with open('app.py', 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Verificar configuraciones críticas
        if 'app = Flask(__name__)' in contenido:
            print("  ✅ Aplicación Flask configurada")
        else:
            print("  ❌ Aplicación Flask no configurada correctamente")
            return False
        
        if "port=8080" in contenido:
            print("  ✅ Puerto 8080 configurado")
        elif "port=5000" in contenido:
            print("  ⚠️  Puerto 5000 configurado (puede requerir firewall)")
        else:
            print("  ❌ Puerto no especificado")
        
        if "host='0.0.0.0'" in contenido:
            print("  ✅ Host configurado para acceso externo")
        else:
            print("  ⚠️  Host no configurado para acceso externo")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error leyendo app.py: {e}")
        return False

def mostrar_comandos_ejecucion():
    """Muestra los comandos para ejecutar la aplicación"""
    print("\n🚀 Comandos para ejecutar el sistema:")
    print("="*50)
    print("📁 Navegar al directorio:")
    print('   cd "c:\\Users\\usuario1\\Documents\\PROY-ESTACIONAMIENTO-PY"')
    print("\n🔧 Activar entorno virtual:")
    print("   .venv\\Scripts\\activate")
    print("\n▶️  Ejecutar aplicación:")
    print("   python app.py")
    print("   # o si python no funciona:")
    print("   .venv\\Scripts\\python.exe app.py")
    print("\n🌐 Acceso web:")
    print("   Local: http://localhost:8080")
    print("   Red:   http://192.168.100.5:8080")
    print("\n⏹️  Detener servidor:")
    print("   Ctrl + C")

def main():
    """Función principal de validación"""
    print("🚗 VALIDADOR DEL SISTEMA DE ESTACIONAMIENTO")
    print("="*60)
    
    # Cambiar al directorio del proyecto
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    validaciones = [
        validar_estructura_archivos(),
        validar_datos_json(),
        validar_imports(),
        validar_configuracion_app()
    ]
    
    print("\n📊 RESUMEN DE VALIDACIÓN")
    print("="*30)
    
    if all(validaciones):
        print("🎉 ¡Todas las validaciones PASARON!")
        print("✅ El sistema está listo para ejecutarse")
        mostrar_comandos_ejecucion()
        return 0
    else:
        print("❌ Algunas validaciones FALLARON")
        print("🔧 Revisa los errores mostrados arriba")
        return 1

if __name__ == "__main__":
    sys.exit(main())