#!/usr/bin/env python3
"""
Script per convertire paintings_add.json a formato multilingua
Converte tutti i campi testo in oggetti {it: "...", en: ""}
"""
import json

def convert_to_multilang(painting):
    """Converte un dipinto al formato multilingua"""
    result = {
        "id": painting["id"],
        "publicationDate": painting.get("publicationDate")
    }

    # Converti TITLE a multilang
    if "title" in painting and painting["title"]:
        result["title"] = {
            "it": painting["title"],
            "en": ""
        }
    else:
        result["title"] = {"it": "", "en": ""}

    # Converti TECHNIQUE a multilang
    if "technique" in painting and painting["technique"]:
        result["technique"] = {
            "it": painting["technique"],
            "en": ""
        }
    else:
        result["technique"] = {"it": "", "en": ""}

    # Mantieni CATEGORY come stringa semplice
    result["category"] = painting.get("category")

    # Mantieni PRICE come stringa semplice
    result["price"] = painting.get("price", "100€")

    # Mantieni DIMENSIONS come stringa semplice
    result["dimensions"] = painting.get("dimensions")

    # Converti DESCRIPTION a multilang
    if "description" in painting and painting["description"]:
        result["description"] = {
            "it": painting["description"],
            "en": ""
        }
    else:
        result["description"] = {"it": "", "en": ""}

    # Rinomina imageLink -> image
    if "imageLink" in painting:
        result["image"] = painting["imageLink"]
    elif "image" in painting:
        result["image"] = painting["image"]
    else:
        result["image"] = None

    return result

def main():
    # Leggi paintings_add.json esistente
    with open('paintings_add.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Estrai array di paintings (potrebbe essere {"paintings": [...]} o solo [...])
    if isinstance(data, dict) and "paintings" in data:
        paintings = data["paintings"]
    elif isinstance(data, list):
        paintings = data
    else:
        print("✗ Formato JSON non riconosciuto")
        return

    # Converti ogni painting
    converted = []
    for painting in paintings:
        converted.append(convert_to_multilang(painting))

    # Ordina per ID
    converted.sort(key=lambda x: x['id'])

    # Salva il risultato
    with open('paintings_add.json', 'w', encoding='utf-8') as f:
        json.dump(converted, f, ensure_ascii=False, indent=2)

    print(f"✓ File paintings_add.json convertito a formato multilingua")
    print(f"  Totale opere: {len(converted)}")
    print(f"  Primo ID: {converted[0]['id']}")
    print(f"  Ultimo ID: {converted[-1]['id']}")

    # Mostra un esempio
    if converted:
        print(f"\nEsempio struttura (ID {converted[0]['id']}):")
        print(f"  title: {converted[0]['title']}")
        print(f"  technique: {converted[0]['technique']}")
        print(f"  image: {converted[0]['image']}")

if __name__ == "__main__":
    main()
