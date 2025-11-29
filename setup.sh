#!/bin/bash

echo "=== AGORA MVP SETUP ==="

# Intră în backend
cd backend

# Șterge venv vechi dacă există
if [ -d "venv" ]; then
    echo "Șterg venv vechi..."
    rm -rf venv
fi

# Găsește Python 3.11
PYTHON311=$(which python3.11)

if [ -z "$PYTHON311" ]; then
    echo "❌ Python 3.11 nu este instalat!"
    echo "Instalează cu: brew install python@3.11"
    exit 1
fi

echo "Folosesc: $PYTHON311"
$PYTHON311 --version

# Creare virtual environment
echo "Creare virtual environment cu Python 3.11..."
$PYTHON311 -m venv venv

# Activare venv
source venv/bin/activate

# Verifică versiunea în venv
echo "Verificare versiune în venv:"
python --version

# Instalare dependențe
echo "Instalare dependențe..."
pip install --upgrade pip
pip install fastapi==0.104.1
pip install uvicorn==0.24.0
pip install anthropic==0.39.0
pip install openai==1.54.0
pip install google-generativeai==0.3.2
pip install httpx==0.27.0

echo ""
echo "✅ Setup complet!"
echo "Rulează: bash run.sh"