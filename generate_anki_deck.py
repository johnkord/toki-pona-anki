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
        {'name': 'SitelenPona'},
        {'name': 'SitelenPonaImage'}
    ],
    templates=[
        {
            'name': 'Word to Sitelen Pona + Definition',
            'qfmt': '{{Word}}',
            'afmt': '<div class="word">{{Word}}</div><br>'
                    '<div class="type">{{Type}}</div><br>'
                    '<div class="definition">{{Definition}}</div><br>'
                    '<hr><div class="sitelen-pona">{{SitelenPona}}</div>'
                    '{{SitelenPonaImage}}',
        },
        {
            'name': 'Definition to Word + Sitelen Pona',
            'qfmt': '<div class="definition">{{Definition}}</div>',
            'afmt': '<div class="word">{{Word}}</div><br>'
                    '<div class="type">{{Type}}</div><br>'
                    '<div class="definition">{{Definition}}</div><br>'
                    '<hr><div class="sitelen-pona">{{SitelenPona}}</div>'
                    '{{SitelenPonaImage}}',
        },
        {
            'name': 'Image to Word + Definition',
            'qfmt': '{{SitelenPonaImage}}',
            'afmt': '<div class="word">{{Word}}</div><br>'
                    '<div class="type">{{Type}}</div><br>'
                    '<div class="definition">{{Definition}}</div><br>'
                    '<hr><div class="sitelen-pona">{{SitelenPona}}</div>'
                    '{{SitelenPonaImage}}',
        },
        {
            'name': 'Word to Definition + Image',
            'qfmt': '<div class="word">{{Word}}</div>',
            'afmt': '<div class="word">{{Word}}</div><br>'
                    '<div class="type">{{Type}}</div><br>'
                    '<div class="definition">{{Definition}}</div><br>'
                    '<hr><div class="sitelen-pona">{{SitelenPona}}</div>'
                    '{{SitelenPonaImage}}',
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
        .sitelen-image {
            width: 180px;
            height: 180px;
            margin: 10px auto;
            display: block;
            border: 1px solid #ddd;
        }
        .no-image {
            color: #999;
            font-style: italic;
            margin: 10px auto;
            text-align: center;
        }
    """
)

def load_sitelen_pona_images(words_data):
    """Load pre-generated sitelen pona images for all words."""
    images_dir = Path("sitelen_pona_images")
    
    if not images_dir.exists():
        print(f"Error: Images directory '{images_dir}' not found.")
        print("Please run 'python generate_images.py' first to generate the images.")
        return {}
    
    print(f"Loading sitelen pona images from: {images_dir}")
    
    # Load images for all words
    word_to_image = {}
    missing_images = []
    
    for word in words_data.keys():
        image_path = images_dir / f"{word}.png"
        if image_path.exists() and os.path.getsize(image_path) > 0:
            word_to_image[word] = str(image_path)
            print(f"✓ Found image for '{word}': {image_path.name}")
        else:
            missing_images.append(word)
            print(f"✗ Missing image for '{word}'")
    
    if missing_images:
        print(f"Warning: {len(missing_images)} images are missing.")
        print("You may need to regenerate images by running: python generate_images.py")
    
    print(f"Loaded {len(word_to_image)} sitelen pona images")
    return word_to_image

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
    
    # Load pre-generated images
    word_to_image = load_sitelen_pona_images(words_data)
    
    # Build media files list for genanki to package
    media_files = []
    
    for word in words_data.keys():
        if word in word_to_image:
            image_path = word_to_image[word]
            if os.path.exists(image_path) and os.path.getsize(image_path) > 0:
                media_files.append(str(image_path))
                print(f"Adding image for '{word}': {os.path.basename(image_path)}")
    
    # Create a note for each word (in random order for better initial presentation)
    words_list = list(words_data.items())
    random.shuffle(words_list)
    
    for word, info in words_list:
        definition = info['definition']
        word_type = info['type']
        
        # Create the image HTML tag if available, otherwise show no-image message
        image_html = ""
        if word in word_to_image:
            image_filename = os.path.basename(word_to_image[word])
            # Use web-compatible img attributes for better AnkiApp support
            image_html = f'<div><img src="{image_filename}" alt="Sitelen pona for {word}" class="sitelen-image" width="180" height="180" style="max-width: 180px; max-height: 180px; display: block; margin: 0 auto;" loading="lazy"></div>'
            print(f"Using image HTML for '{word}': {image_filename}")
        else:
            image_html = f'<div class="no-image">No image available for {word}</div>'
        
        # Create the note with all fields
        note = genanki.Note(
            model=TOKI_PONA_MODEL,
            fields=[word, definition, word_type, word, image_html]
        )
        deck.add_note(note)
    
    # Create the Anki package
    anki_package = genanki.Package(deck)
    
    if media_files:
        anki_package.media_files = media_files
        print(f"Added {len(media_files)} media files to Anki package")
    
    anki_package.write_to_file(OUTPUT_FILE)
    print(f"Anki deck created: {OUTPUT_FILE}")
    print(f"Number of cards: {len(words_data) * 4}")  # Four card types per word
    
    # Add a helpful message about missing images
    print("\nNotes:")
    print("- If Sitelen Pona images aren't showing in Anki after importing the deck:")
    print("  1. In Anki, go to Tools > Check Media")
    print("  2. Close and restart Anki")
    print("  3. Make sure all images were included in the package")
    print("- To regenerate images, run: python generate_images.py")
    print("- Images are located in the 'sitelen_pona_images' directory")

if __name__ == "__main__":
    create_anki_deck()