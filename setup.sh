#!/bin/bash

# Vytvoření virtuálního prostředí
python3 -m venv venv
source venv/bin/activate

# Instalace závislostí
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Prostředí připraveno. Aktivujte ho: source venv/bin/activate"
