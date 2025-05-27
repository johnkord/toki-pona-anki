#!/usr/bin/env python3
"""
Script to generate an Anki deck for Toki Pona with Sitelen Pona characters.

This script reads a JSON file containing Toki Pona words and their definitions,
then creates an Anki deck with cards for each word. The front of each card
shows the word in Sitelen Pona, and the back shows the word in Latin script
along with its definition.
"""

import json
import os
import random
import genanki
import requests
import tempfile
from pathlib import Path

# Constants
MODEL_ID = random.randrange(1 << 30, 1 << 31)
DECK_ID = random.randrange(1 << 30, 1 << 31)
OUTPUT_FILE = "toki_pona_sitelen_pona.apkg"

# Model for Anki cards
TOKI_PONA_MODEL = genanki.Model(
    MODEL_ID,
    'Toki Pona Sitelen Pona Model',
    fields=[
        {'name': 'Word'},
        {'name': 'Definition'},
        {'name': 'Type'},
        {'name': 'SitelenPona'}
    ],
    templates=[
        {
            'name': 'Sitelen Pona to Word + Definition',
            'qfmt': '{{SitelenPona}}',
            'afmt': '<div class="word">{{Word}}</div><br>'
                    '<div class="type">{{Type}}</div><br>'
                    '<div class="definition">{{Definition}}</div><br>'
                    '<hr><div class="sitelen-pona">{{SitelenPona}}</div>',
        },
        {
            'name': 'Word to Sitelen Pona + Definition',
            'qfmt': '{{Word}}',
            'afmt': '<div class="word">{{Word}}</div><br>'
                    '<div class="type">{{Type}}</div><br>'
                    '<div class="definition">{{Definition}}</div><br>'
                    '<hr><div class="sitelen-pona">{{SitelenPona}}</div>',
        }
    ],
    css="""
        .card {
            font-family: arial;
            font-size: 20px;
            text-align: center;
            color: black;
            background-color: white;
        }
        .word {
            font-size: 28px;
            font-weight: bold;
        }
        .type {
            font-style: italic;
            color: #666;
        }
        .definition {
            font-size: 22px;
        }
        .sitelen-pona {
            font-family: "linja-pona", "linjapona", "sitelen pona";
            font-size: 60px;
        }
    """
)

def download_font():
    """Download the linjapona font for Sitelen Pona if not already present."""
    font_dir = Path("fonts")
    font_path = font_dir / "linjapona.otf"
    
    if font_path.exists():
        return font_path
    
    font_dir.mkdir(exist_ok=True)
    
    # Try different font sources
    font_urls = [
        "https://github.com/kreativekorp/linja-pona/raw/master/linja-pona-4.9.otf",
        "https://wyub.github.io/tokipona/linja-pona-4.9.otf"
    ]
    
    for font_url in font_urls:
        try:
            print(f"Attempting to download font from: {font_url}")
            response = requests.get(font_url)
            response.raise_for_status()
            
            with open(font_path, 'wb') as f:
                f.write(response.content)
            
            print(f"Downloaded font to {font_path}")
            return font_path
        
        except Exception as e:
            print(f"Failed to download font from {font_url}: {e}")
    
    print("\nCould not download a Sitelen Pona font.")
    print("You'll need to manually add a Sitelen Pona font to your Anki collection.")
    print("Fonts can be found at: https://github.com/kreativekorp/linja-pona")
    return None

def create_anki_deck():
    """Create an Anki deck with Toki Pona words and Sitelen Pona characters."""
    # Load words data
    with open('toki_pona_words.json', 'r', encoding='utf-8') as f:
        words_data = json.load(f)
    
    # Create the deck
    deck = genanki.Deck(
        DECK_ID,
        'Toki Pona - Sitelen Pona'
    )
    
    # Create a note for each word
    for word, info in words_data.items():
        definition = info['definition']
        word_type = info['type']
        
        # The Sitelen Pona character is represented by the word itself
        # when using a Sitelen Pona font
        note = genanki.Note(
            model=TOKI_PONA_MODEL,
            fields=[word, definition, word_type, word]
        )
        deck.add_note(note)
    
    # Create the Anki package
    font_path = download_font()
    anki_package = genanki.Package(deck)
    
    if font_path and font_path.exists():
        anki_package.media_files = [str(font_path)]
    
    anki_package.write_to_file(OUTPUT_FILE)
    print(f"Anki deck created: {OUTPUT_FILE}")
    print(f"Number of cards: {len(words_data)}")

if __name__ == "__main__":
    create_anki_deck()