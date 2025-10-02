#!/bin/bash
# Script para compartir usando SSH tunnel (Serveo)

echo "🌐 Creando túnel público para el sistema de estacionamiento..."
echo "Presiona Ctrl+C para detener el túnel"
echo ""

# Crear túnel SSH usando serveo.net
ssh -R 80:localhost:8080 serveo.net