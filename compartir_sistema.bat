@echo off
title Compartir Sistema de Estacionamiento
echo.
echo 🌐 COMPARTIR SISTEMA DE ESTACIONAMIENTO CON EL MUNDO
echo =====================================================
echo.
echo Opciones disponibles:
echo.
echo 1. Ngrok (Gratis, Fácil)
echo 2. Serveo (Gratis, Sin registro)
echo 3. Localhost.run (Gratis)
echo 4. Manual - IP Pública
echo 5. Salir
echo.
set /p opcion="Selecciona una opción (1-5): "

if "%opcion%"=="1" goto ngrok
if "%opcion%"=="2" goto serveo
if "%opcion%"=="3" goto localhost_run
if "%opcion%"=="4" goto manual
if "%opcion%"=="5" goto salir

:ngrok
echo.
echo 📋 INSTRUCCIONES PARA NGROK:
echo =============================
echo 1. Ve a: https://ngrok.com/
echo 2. Crea una cuenta gratuita
echo 3. Descarga ngrok.exe
echo 4. Copia ngrok.exe a esta carpeta
echo 5. En nueva terminal ejecuta: ngrok http 8080
echo 6. Comparte la URL que aparece (ej: https://abc123.ngrok.io)
echo.
echo ✅ Ventajas: Fácil, HTTPS, Estable
echo ⚠️  Límite: 20 conexiones gratis
echo.
pause
goto menu

:serveo
echo.
echo 📋 INSTRUCCIONES PARA SERVEO:
echo ============================
echo 1. Abrir nueva terminal (CMD)
echo 2. Ejecutar: ssh -R 80:localhost:8080 serveo.net
echo 3. Aparecerá una URL pública (ej: https://abc123.serveo.net)
echo 4. Compartir esa URL
echo.
echo ✅ Ventajas: Sin registro, Gratis
echo ⚠️  Desventaja: Puede ser inestable
echo.
pause
goto menu

:localhost_run
echo.
echo 📋 INSTRUCCIONES PARA LOCALHOST.RUN:
echo ==================================
echo 1. Abrir nueva terminal (CMD)
echo 2. Ejecutar: ssh -R 80:localhost:8080 localhost.run
echo 3. Aparecerá una URL pública
echo 4. Compartir esa URL
echo.
echo ✅ Ventajas: Sin registro
echo ⚠️  Puede requerir configuración SSH
echo.
pause
goto menu

:manual
echo.
echo 📋 CONFIGURACIÓN MANUAL:
echo =======================
echo 1. Configurar Port Forwarding en tu router (Puerto 8080)
echo 2. Obtener tu IP pública: https://whatismyipaddress.com
echo 3. Compartir: http://TU_IP_PUBLICA:8080
echo.
echo ⚠️  RIESGO: Expones tu red directamente
echo ⚠️  Requiere conocimientos de redes
echo.
pause
goto menu

:salir
echo.
echo 👋 ¡Hasta luego!
exit

:menu
cls
goto inicio