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
from PIL import Image, ImageDraw, ImageFont

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
            'name': 'Sitelen Pona to Word + Definition',
            'qfmt': '<div class="sitelen-pona">{{SitelenPona}}</div><br>'
                    '<div><img src="{{SitelenPonaImage}}" class="sitelen-image"></div>',
            'afmt': '<div class="word">{{Word}}</div><br>'
                    '<div class="type">{{Type}}</div><br>'
                    '<div class="definition">{{Definition}}</div><br>'
                    '<hr><div class="sitelen-pona">{{SitelenPona}}</div>'
                    '<div><img src="{{SitelenPonaImage}}" class="sitelen-image"></div>',
        },
        {
            'name': 'Word to Sitelen Pona + Definition',
            'qfmt': '{{Word}}',
            'afmt': '<div class="word">{{Word}}</div><br>'
                    '<div class="type">{{Type}}</div><br>'
                    '<div class="definition">{{Definition}}</div><br>'
                    '<hr><div class="sitelen-pona">{{SitelenPona}}</div>'
                    '<div><img src="{{SitelenPonaImage}}" class="sitelen-image"></div>',
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
            max-width: 180px;
            max-height: 180px;
            margin: 10px auto;
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

def generate_sitelen_pona_image(word, font_path, output_dir, size=(200, 200)):
    """Generate an image for a sitelen pona character."""
    if not font_path or not font_path.exists():
        print(f"Font file not found at {font_path}")
        return None
    
    # Create a new image with white background
    img = Image.new('RGB', size, color='white')
    draw = ImageDraw.Draw(img)
    
    # Try to load the font
    try:
        font = ImageFont.truetype(str(font_path), size=int(min(size) * 0.7))
    except Exception as e:
        print(f"Error loading font for image generation: {e}")
        return None
    
    # Calculate text position to center it
    left, top, right, bottom = draw.textbbox((0, 0), word, font=font)
    text_width = right - left
    text_height = bottom - top
    position = ((size[0] - text_width) / 2, (size[1] - text_height) / 2)
    
    # Draw the text
    draw.text(position, word, font=font, fill='black')
    
    # Save the image
    output_file = os.path.join(output_dir, f"{word}.png")
    img.save(output_file)
    
    return output_file

def generate_sitelen_pona_images(words_data, font_path):
    """Generate sitelen pona images for all words."""
    if not font_path or not font_path.exists():
        print("Font not available, skipping image generation.")
        return {}
    
    # Create a temporary directory for the images
    image_dir = Path(tempfile.mkdtemp(prefix="sitelen_pona_"))
    print(f"Generating sitelen pona images in: {image_dir}")
    
    # Generate images for all words
    word_to_image = {}
    for word in words_data.keys():
        try:
            image_path = generate_sitelen_pona_image(word, font_path, image_dir)
            if image_path:
                word_to_image[word] = image_path
        except Exception as e:
            print(f"Error generating image for '{word}': {e}")
    
    print(f"Generated {len(word_to_image)} sitelen pona images")
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
    
    # Download the font and generate images
    font_path = download_font()
    word_to_image = {}
    if font_path and font_path.exists():
        word_to_image = generate_sitelen_pona_images(words_data, font_path)
    
    # Create a note for each word
    for word, info in words_data.items():
        definition = info['definition']
        word_type = info['type']
        
        # Get the image filename if available, otherwise empty string
        image_filename = ""
        if word in word_to_image:
            image_filename = os.path.basename(word_to_image[word])
        
        # Create the note with all fields
        note = genanki.Note(
            model=TOKI_PONA_MODEL,
            fields=[word, definition, word_type, word, image_filename]
        )
        deck.add_note(note)
    
    # Create the Anki package
    anki_package = genanki.Package(deck)
    media_files = []
    
    # Add the font to media files if available
    if font_path and font_path.exists():
        media_files.append(str(font_path))
    
    # Add all generated images to media files
    media_files.extend([str(path) for path in word_to_image.values()])
    
    if media_files:
        anki_package.media_files = media_files
    
    anki_package.write_to_file(OUTPUT_FILE)
    print(f"Anki deck created: {OUTPUT_FILE}")
    print(f"Number of cards: {len(words_data) * 2}")  # Two card types per word

if __name__ == "__main__":
    create_anki_deck()