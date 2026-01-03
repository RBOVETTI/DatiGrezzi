#!/usr/bin/env python3
"""
Script per creare paintings_add.json con tutti gli ID da 1 a 99
"""
import json
import re

def extract_painting_data(block, painting_id):
    """Estrae i dati di un'opera da un blocco di testo"""
    data = {"id": painting_id}

    # Estrai DATA PUBBLICAZIONE
    match = re.search(r'DATA PUBBLICAZIONE:\s*(.+)', block)
    data["publicationDate"] = match.group(1).strip() if match else None

    # Estrai TITOLO
    match = re.search(r'TITOLO:\s*(.+)', block)
    data["title"] = match.group(1).strip() if match else None

    # Estrai TECNICA
    match = re.search(r'TECNICA:\s*(.+)', block)
    data["technique"] = match.group(1).strip() if match and match.group(1).strip() != 'nan' else None

    # Estrai DIMENSIONI
    match = re.search(r'DIMENSIONI:\s*(.+)', block)
    dims = match.group(1).strip() if match else None
    data["dimensions"] = None if not dims or dims == 'nan' else dims

    # Estrai DESCRIZIONE
    match = re.search(r'DESCRIZIONE:\s*(.+?)(?=\nLINK IMMAGINE:|\n---|\Z)', block, re.DOTALL)
    if match:
        desc = match.group(1).strip()
        data["description"] = None if desc == 'nan' else desc
    else:
        data["description"] = None

    # Estrai LINK IMMAGINE
    match = re.search(r'LINK IMMAGINE:\s*(.+)', block)
    data["imageLink"] = match.group(1).strip() if match else None

    # Estrai CATEGORIA
    match = re.search(r'CATEGORIA:\s*(.+)', block)
    cat = match.group(1).strip() if match else None
    data["category"] = None if not cat or cat == '-' else cat

    # Estrai PREZZO
    match = re.search(r'PREZZO:\s*(.+)', block)
    data["price"] = match.group(1).strip() if match else "100€"

    return data

def main():
    # Leggi il file opere_formattate.txt
    with open('opere_formattate.txt', 'r', encoding='utf-8') as f:
        content = f.read()

    # Dividi in blocchi
    blocks = content.split('---')

    paintings = []

    for block in blocks:
        if not block.strip():
            continue

        # Cerca ID
        id_match = re.search(r'^ID:\s*(\d+)', block, re.MULTILINE)
        if not id_match:
            continue

        painting_id = int(id_match.group(1))

        # Processa solo ID da 1 a 99
        if 1 <= painting_id <= 99:
            painting_data = extract_painting_data(block, painting_id)
            paintings.append(painting_data)

    # Ordina per ID
    paintings.sort(key=lambda x: x['id'])

    # Crea il JSON finale
    result = {"paintings": paintings}

    # Salva in paintings_add.json
    with open('paintings_add.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"✓ File paintings_add.json creato con {len(paintings)} opere (ID 1-99)")
    print(f"  Primo ID: {paintings[0]['id']}")
    print(f"  Ultimo ID: {paintings[-1]['id']}")

if __name__ == "__main__":
    main()
