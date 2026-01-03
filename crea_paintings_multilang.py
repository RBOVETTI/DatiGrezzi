#!/usr/bin/env python3
"""
Script per creare paintings_add.json con struttura multilingua completa
- ID 1-40: dati originali con traduzioni esistenti
- ID 41-99: dati da opere_formattate.txt con it compilato e en vuoto
"""
import json
import re

# Dati originali ID 1-40 forniti dall'utente
ORIGINAL_PAINTINGS = []  # Verrà popolato dal file JSON originale se esiste

def extract_painting_data_multilang(block, painting_id):
    """Estrae i dati di un'opera da un blocco di testo in formato multilingua"""
    data = {"id": painting_id}

    # Estrai DATA PUBBLICAZIONE
    match = re.search(r'DATA PUBBLICAZIONE:\s*(.+)', block)
    data["publicationDate"] = match.group(1).strip() if match else None

    # Estrai TITOLO (multilingua con en vuoto)
    match = re.search(r'TITOLO:\s*(.+)', block)
    if match:
        data["title"] = {
            "it": match.group(1).strip(),
            "en": ""
        }
    else:
        data["title"] = {"it": "", "en": ""}

    # Estrai TECNICA (multilingua con en vuoto)
    match = re.search(r'TECNICA:\s*(.+)', block)
    if match and match.group(1).strip() != 'nan':
        data["technique"] = {
            "it": match.group(1).strip(),
            "en": ""
        }
    else:
        data["technique"] = {"it": "", "en": ""}

    # Estrai CATEGORIA
    match = re.search(r'CATEGORIA:\s*(.+)', block)
    cat = match.group(1).strip() if match else None
    data["category"] = None if not cat or cat == '-' else cat

    # Estrai PREZZO
    match = re.search(r'PREZZO:\s*(.+)', block)
    data["price"] = match.group(1).strip() if match else "100€"

    # Estrai DIMENSIONI
    match = re.search(r'DIMENSIONI:\s*(.+)', block)
    dims = match.group(1).strip() if match else None
    data["dimensions"] = None if not dims or dims == 'nan' else dims

    # Estrai DESCRIZIONE (multilingua con en vuoto)
    match = re.search(r'DESCRIZIONE:\s*(.+?)(?=\nLINK IMMAGINE:|\n---|\Z)', block, re.DOTALL)
    if match:
        desc = match.group(1).strip()
        data["description"] = {
            "it": desc if desc != 'nan' else "",
            "en": ""
        }
    else:
        data["description"] = {"it": "", "en": ""}

    # Estrai LINK IMMAGINE (campo chiamato "image")
    match = re.search(r'LINK IMMAGINE:\s*(.+)', block)
    data["image"] = match.group(1).strip() if match else None

    return data

def main():
    # Leggi i dati originali ID 1-40 dal JSON fornito
    paintings_1_40_json = """[inserire qui il JSON dei primi 40]"""

    # Per ora li carico da file se esiste, altrimenti uso array vuoto
    try:
        with open('paintings_original_40.json', 'r', encoding='utf-8') as f:
            paintings_1_40 = json.load(f)
    except:
        print("⚠ File paintings_original_40.json non trovato")
        print("  Usando solo dati da opere_formattate.txt per ID 1-40")
        paintings_1_40 = []

    # Leggi il file opere_formattate.txt per ID 41-99
    with open('opere_formattate.txt', 'r', encoding='utf-8') as f:
        content = f.read()

    # Dividi in blocchi
    blocks = content.split('---')

    paintings_41_99 = []

    for block in blocks:
        if not block.strip():
            continue

        # Cerca ID
        id_match = re.search(r'^ID:\s*(\d+)', block, re.MULTILINE)
        if not id_match:
            continue

        painting_id = int(id_match.group(1))

        # Processa solo ID da 41 a 99
        if 41 <= painting_id <= 99:
            painting_data = extract_painting_data_multilang(block, painting_id)
            paintings_41_99.append(painting_data)
        # Se non abbiamo i dati originali, estrai anche 1-40
        elif 1 <= painting_id <= 40 and not paintings_1_40:
            painting_data = extract_painting_data_multilang(block, painting_id)
            paintings_1_40.append(painting_data)

    # Ordina per ID
    paintings_1_40.sort(key=lambda x: x['id'])
    paintings_41_99.sort(key=lambda x: x['id'])

    # Unisci tutto
    all_paintings = paintings_1_40 + paintings_41_99

    # Salva in paintings_add.json
    with open('paintings_add.json', 'w', encoding='utf-8') as f:
        json.dump(all_paintings, f, ensure_ascii=False, indent=2)

    print(f"✓ File paintings_add.json creato con {len(all_paintings)} opere")
    print(f"  - ID 1-40: {len(paintings_1_40)} opere")
    print(f"  - ID 41-99: {len(paintings_41_99)} opere")
    if all_paintings:
        print(f"  Primo ID: {all_paintings[0]['id']}")
        print(f"  Ultimo ID: {all_paintings[-1]['id']}")

if __name__ == "__main__":
    main()
