#!/usr/bin/env python3
"""
Script per rinominare le immagini delle opere aggiungendo il prefisso ID_
"""
import os
import re
import shutil

def main():
    # Path dei file
    txt_file = "opere_formattate.txt"
    img_dir = "IMG"
    backup_file = "opere_formattate.txt.backup"

    # Crea backup del file originale
    shutil.copy2(txt_file, backup_file)
    print(f"✓ Backup creato: {backup_file}")

    # Leggi il contenuto del file
    with open(txt_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Dividi in blocchi usando --- come separatore
    blocks = content.split('---')

    modifiche = []
    errori = []
    gia_rinominate = []

    for block in blocks:
        if not block.strip():
            continue

        # Cerca ID
        id_match = re.search(r'^ID:\s*(\d+)', block, re.MULTILINE)
        if not id_match:
            continue

        opera_id = id_match.group(1)

        # Cerca LINK IMMAGINE
        img_match = re.search(r'^LINK IMMAGINE:\s*(.+)$', block, re.MULTILINE)
        if not img_match:
            continue

        img_path = img_match.group(1).strip()

        # Verifica se l'immagine ha già il prefisso ID_
        filename = os.path.basename(img_path)
        dirname = os.path.dirname(img_path)

        if filename.startswith(f"{opera_id}_"):
            gia_rinominate.append(f"ID {opera_id}: {img_path} (già rinominata)")
            continue

        # Costruisci il nuovo nome
        new_filename = f"{opera_id}_{filename}"
        new_img_path = os.path.join(dirname, new_filename)

        # Path completi per il file system
        old_file_path = img_path
        new_file_path = new_img_path

        # Verifica che il file esista
        if not os.path.exists(old_file_path):
            errori.append(f"ID {opera_id}: File non trovato: {old_file_path}")
            continue

        # Verifica che il nuovo nome non esista già
        if os.path.exists(new_file_path):
            errori.append(f"ID {opera_id}: Il file di destinazione esiste già: {new_file_path}")
            continue

        # Rinomina il file
        try:
            os.rename(old_file_path, new_file_path)

            # Aggiorna il contenuto del testo
            content = content.replace(
                f"LINK IMMAGINE: {img_path}",
                f"LINK IMMAGINE: {new_img_path}"
            )

            modifiche.append(f"ID {opera_id}: {img_path} → {new_img_path}")
        except Exception as e:
            errori.append(f"ID {opera_id}: Errore durante rinomina: {e}")

    # Salva il file aggiornato
    if modifiche:
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n✓ File {txt_file} aggiornato")

    # Report
    print("\n" + "="*70)
    print("REPORT RINOMINA IMMAGINI")
    print("="*70)

    if modifiche:
        print(f"\n✓ MODIFICHE EFFETTUATE ({len(modifiche)}):")
        for m in modifiche:
            print(f"  - {m}")

    if gia_rinominate:
        print(f"\n○ GIÀ RINOMINATE ({len(gia_rinominate)}):")
        for g in gia_rinominate:
            print(f"  - {g}")

    if errori:
        print(f"\n✗ ERRORI ({len(errori)}):")
        for e in errori:
            print(f"  - {e}")

    print("\n" + "="*70)
    print(f"Totale blocchi processati: {len(blocks)-1}")
    print(f"Modifiche: {len(modifiche)} | Già OK: {len(gia_rinominate)} | Errori: {len(errori)}")
    print("="*70)

if __name__ == "__main__":
    main()
