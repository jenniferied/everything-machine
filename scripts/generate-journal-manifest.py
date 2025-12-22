#!/usr/bin/env python3
"""
Generiert automatisch ein Manifest aller Journal-Einträge im journal/ Ordner
Kann manuell ausgeführt oder in einen Build-Prozess integriert werden
"""

import os
import json
from pathlib import Path

JOURNAL_DIR = Path(__file__).parent / 'journal'
OUTPUT_FILE = Path(__file__).parent / 'journal-manifest.json'

try:
    # Lese alle .md Dateien aus dem journal/ Ordner
    files = sorted([
        f'journal/{file.name}'
        for file in JOURNAL_DIR.glob('*.md')
        if file.name.startswith('journal-')
    ])
    
    # Schreibe Manifest
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(files, f, indent=2, ensure_ascii=False)
    
    print(f'✓ Journal-Manifest erstellt mit {len(files)} Einträgen:')
    for file in files:
        print(f'  - {file}')
    print(f'\nGeschrieben nach: {OUTPUT_FILE}')
    
except Exception as error:
    print(f'Fehler beim Erstellen des Manifests: {error}')
    exit(1)

