@echo off
echo 🌐 Creando túnel público para el sistema de estacionamiento...
echo Presiona Ctrl+C para detener el túnel
echo.
echo IMPORTANTE: Mantén el servidor Flask corriendo en otra terminal
echo.
pause

REM Usar serveo.net para crear túnel público
ssh -R 80:localhost:8080 serveo.net