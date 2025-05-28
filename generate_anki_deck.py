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
                    '{{#SitelenPonaImage}}<div><img src="{{SitelenPonaImage}}" alt="{{Word}}" class="sitelen-image" width="180" height="180"></div>{{/SitelenPonaImage}}'
                    '{{^SitelenPonaImage}}<div class="no-image">No image available for {{Word}}</div>{{/SitelenPonaImage}}',
            'afmt': '<div class="word">{{Word}}</div><br>'
                    '<div class="type">{{Type}}</div><br>'
                    '<div class="definition">{{Definition}}</div><br>'
                    '<hr><div class="sitelen-pona">{{SitelenPona}}</div>'
                    '{{#SitelenPonaImage}}<div><img src="{{SitelenPonaImage}}" alt="{{Word}}" class="sitelen-image" width="180" height="180"></div>{{/SitelenPonaImage}}'
                    '{{^SitelenPonaImage}}<div class="no-image">No image available for {{Word}}</div>{{/SitelenPonaImage}}',
        },
        {
            'name': 'Word to Sitelen Pona + Definition',
            'qfmt': '{{Word}}',
            'afmt': '<div class="word">{{Word}}</div><br>'
                    '<div class="type">{{Type}}</div><br>'
                    '<div class="definition">{{Definition}}</div><br>'
                    '<hr><div class="sitelen-pona">{{SitelenPona}}</div>'
                    '{{#SitelenPonaImage}}<div><img src="{{SitelenPonaImage}}" alt="{{Word}}" class="sitelen-image" width="180" height="180"></div>{{/SitelenPonaImage}}'
                    '{{^SitelenPonaImage}}<div class="no-image">No image available for {{Word}}</div>{{/SitelenPonaImage}}',
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

def download_font():
    """Download the linjapona font for Sitelen Pona if not already present."""
    font_dir = Path("fonts")
    font_path = font_dir / "linjapona.otf"
    
    if font_path.exists() and os.path.getsize(font_path) > 0:
        print(f"Using existing font: {font_path}")
        return font_path
    
    font_dir.mkdir(exist_ok=True)
    
    # Try different font sources - updated with more recent URLs
    font_urls = [
        "https://github.com/lipu-linku/ijo/raw/main/o_lukin/linku_ilo/linja-pona.ttf",
        "https://github.com/janSame/linja-pona/raw/main/linja-pona-4.9.otf",
        "https://github.com/lipu-linku/ijo/raw/main/fonts/linja-pona.otf",
        "https://raw.githubusercontent.com/lipu-linku/ijo/main/fonts/linja-pona.otf",
        "https://github.com/kreativekorp/linja-pona/raw/master/linja-pona-4.9.otf",
        "https://wyub.github.io/tokipona/linja-pona-4.9.otf",
        "https://www.kreativekorp.com/software/fonts/linjapona/linja-pona-4.9.otf"
    ]
    
    for font_url in font_urls:
        try:
            print(f"Attempting to download font from: {font_url}")
            response = requests.get(font_url)
            response.raise_for_status()
            
            # Verify we got actual binary content with some minimum size
            if len(response.content) < 1000:  # Basic size check for font files
                print(f"Downloaded content is too small to be a valid font file: {len(response.content)} bytes")
                continue
                
            # Ensure the file has the correct extension based on URL
            if font_url.endswith('.ttf'):
                font_path = font_dir / "linjapona.ttf"
            elif font_url.endswith('.otf'):
                font_path = font_dir / "linjapona.otf"
            
            with open(font_path, 'wb') as f:
                f.write(response.content)
            
            print(f"Downloaded font to {font_path} ({len(response.content)} bytes)")
            return font_path
        
        except Exception as e:
            print(f"Failed to download font from {font_url}: {e}")
    
    print("\nAttempting to find a locally installed Sitelen Pona font...")
    
    # Try to locate a manually installed Sitelen Pona font in common locations
    local_font_paths = [
        Path.home() / "Library/Fonts/linjapona.otf",  # macOS
        Path.home() / "Library/Fonts/linja-pona.otf",
        Path.home() / ".fonts/linjapona.otf",  # Linux
        Path.home() / ".fonts/linja-pona.otf",
        Path("/usr/local/share/fonts/linjapona.otf"),
        Path("/usr/local/share/fonts/linja-pona.otf"),
    ]
    
    for local_path in local_font_paths:
        if local_path.exists() and os.path.getsize(local_path) > 0:
            print(f"Found local Sitelen Pona font: {local_path}")
            # Copy the font to our fonts directory
            with open(local_path, 'rb') as src, open(font_path, 'wb') as dst:
                dst.write(src.read())
            return font_path
    
    # Create a sample image - this isn't ideal but ensures images are created
    print("\nCreating a placeholder font for Sitelen Pona images...")
    # Using a font that's likely to be available on most systems
    fallback_fonts = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans.ttf"
    ]
    
    for fallback_font in fallback_fonts:
        if os.path.exists(fallback_font) and os.path.getsize(fallback_font) > 0:
            print(f"Using fallback font for testing: {fallback_font}")
            return Path(fallback_font)
    
    print("\nCould not find any usable font.")
    print("You'll need to manually add a Sitelen Pona font to your Anki collection.")
    print("Fonts can be found at: https://github.com/kreativekorp/linja-pona")
    return None

def generate_geometric_sitelen_pona(word, size=(200, 200)):
    """Generate a simple geometric representation for sitelen pona when font is not available."""
    img = Image.new('RGB', size, color='white')
    draw = ImageDraw.Draw(img)
    
    # Define geometric shapes for common words based on sitelen pona concepts
    geometric_shapes = {
        'a': lambda: draw.ellipse([50, 80, 150, 120], fill='black'),  # Horizontal oval (vocative)
        'mi': lambda: draw.polygon([(100, 40), (60, 160), (140, 160)], fill='black'),  # Triangle pointing up (I/me)
        'sina': lambda: draw.polygon([(100, 160), (60, 40), (140, 40)], fill='black'),  # Triangle pointing down (you)
        'ona': lambda: draw.ellipse([70, 70, 130, 130], fill='black'),  # Circle (he/she/it)
        'ni': lambda: draw.rectangle([80, 80, 120, 120], fill='black'),  # Square (this/that)
        'pona': lambda: [
            draw.ellipse([70, 70, 130, 130], outline='black', width=3),
            draw.ellipse([90, 90, 110, 110], fill='black')
        ],  # Circle with dot (good)
        'ike': lambda: [
            draw.line([(70, 70), (130, 130)], fill='black', width=4),
            draw.line([(70, 130), (130, 70)], fill='black', width=4)
        ],  # X shape (bad)
        'jan': lambda: [
            draw.ellipse([85, 60, 115, 90], fill='black'),  # Head
            draw.rectangle([95, 90, 105, 140], fill='black')  # Body
        ],  # Stick figure (person)
        'meli': lambda: [
            draw.ellipse([85, 60, 115, 90], fill='black'),  # Head
            draw.rectangle([95, 90, 105, 140], fill='black'),  # Body
            draw.polygon([(80, 140), (120, 140), (100, 160)], fill='black')  # Skirt
        ],  # Female symbol
        'mije': lambda: [
            draw.ellipse([85, 60, 115, 90], fill='black'),  # Head
            draw.rectangle([95, 90, 105, 140], fill='black'),  # Body
            draw.rectangle([85, 130, 95, 140], fill='black'),  # Left leg
            draw.rectangle([105, 130, 115, 140], fill='black')  # Right leg
        ],  # Male symbol
        'moku': lambda: draw.ellipse([70, 100, 130, 160], fill='black'),  # Bowl shape (food)
        'tomo': lambda: [
            draw.rectangle([60, 100, 140, 160], fill='black'),  # House base
            draw.polygon([(60, 100), (100, 60), (140, 100)], fill='black')  # Roof
        ],  # House shape
        'suno': lambda: [
            draw.ellipse([80, 80, 120, 120], fill='black'),  # Sun center
            # Sun rays
            draw.line([(100, 40), (100, 60)], fill='black', width=3),
            draw.line([(100, 140), (100, 160)], fill='black', width=3),
            draw.line([(40, 100), (60, 100)], fill='black', width=3),
            draw.line([(140, 100), (160, 100)], fill='black', width=3),
            draw.line([(65, 65), (75, 75)], fill='black', width=3),
            draw.line([(125, 125), (135, 135)], fill='black', width=3),
            draw.line([(135, 65), (125, 75)], fill='black', width=3),
            draw.line([(75, 125), (65, 135)], fill='black', width=3)
        ],  # Sun with rays
        'mun': lambda: [
            draw.ellipse([70, 70, 130, 130], outline='black', width=3),
            draw.ellipse([80, 80, 120, 120], fill='white')
        ],  # Crescent moon
        'telo': lambda: [
            draw.arc([70, 60, 130, 120], 0, 180, fill='black', width=4),
            draw.arc([75, 90, 125, 150], 0, 180, fill='black', width=4),
            draw.arc([80, 120, 120, 180], 0, 180, fill='black', width=4)
        ],  # Water waves
        'sike': lambda: draw.ellipse([60, 60, 140, 140], outline='black', width=4),  # Circle (round)
        'luka': lambda: [
            draw.rectangle([90, 100, 110, 140], fill='black'),  # Palm
            # Fingers
            draw.rectangle([85, 90, 95, 120], fill='black'),
            draw.rectangle([95, 85, 105, 115], fill='black'),
            draw.rectangle([105, 85, 115, 115], fill='black'),
            draw.rectangle([115, 90, 125, 120], fill='black')
        ],  # Hand
        'kili': lambda: draw.ellipse([75, 75, 125, 125], fill='black'),  # Fruit (circle)
        'kala': lambda: [
            draw.ellipse([60, 85, 120, 115], fill='black'),  # Fish body
            draw.polygon([(120, 100), (140, 90), (140, 110)], fill='black')  # Tail
        ],  # Fish
        'waso': lambda: [
            draw.ellipse([85, 90, 115, 110], fill='black'),  # Bird body
            draw.polygon([(85, 100), (70, 95), (70, 105)], fill='black'),  # Beak
            draw.line([(100, 110), (100, 130)], fill='black', width=3),  # Leg
            draw.line([(95, 130), (105, 130)], fill='black', width=3)  # Foot
        ],  # Bird
        'len': lambda: draw.rectangle([70, 80, 130, 120], fill='black'),  # Clothing (rectangle)
        'lape': lambda: [
            draw.ellipse([85, 90, 115, 110], fill='black'),  # Sleeping body
            draw.arc([80, 70, 100, 90], 0, 180, fill='black', width=3)  # Sleep symbol
        ],  # Sleep
        'utala': lambda: [
            draw.line([(60, 80), (140, 80)], fill='black', width=4),  # Sword blade
            draw.rectangle([95, 80, 105, 100], fill='black')  # Handle
        ],  # Fight/weapon
        'ilo': lambda: [
            draw.rectangle([80, 70, 120, 90], fill='black'),  # Tool head
            draw.rectangle([95, 90, 105, 130], fill='black')  # Handle
        ],  # Tool
        'lipu': lambda: draw.rectangle([70, 60, 130, 140], outline='black', width=3),  # Paper/book
        'olin': lambda: [
            draw.arc([80, 80, 120, 120], 200, 340, fill='black', width=3),  # Heart shape
            draw.polygon([(100, 115), (85, 95), (115, 95)], fill='black')
        ],  # Love/heart
        'wile': lambda: [
            draw.ellipse([85, 85, 115, 115], outline='black', width=3),
            draw.polygon([(100, 85), (95, 75), (105, 75)], fill='black')  # Want/desire (circle with arrow up)
        ],
        'ken': lambda: [
            draw.rectangle([80, 80, 120, 120], outline='black', width=3),
            draw.line([(90, 90), (110, 110)], fill='black', width=3)  # Can/able (square with diagonal)
        ],
        'seli': lambda: [
            draw.polygon([(100, 60), (90, 90), (95, 100), (105, 100), (110, 90)], fill='black'),  # Flame
            draw.ellipse([85, 100, 115, 130], fill='black')  # Fire base
        ],  # Fire/heat
        'lete': lambda: [
            draw.polygon([(100, 60), (95, 80), (105, 80)], fill='black'),  # Icicle
            draw.polygon([(90, 90), (85, 110), (95, 110)], fill='black'),
            draw.polygon([(110, 90), (105, 110), (115, 110)], fill='black')
        ],  # Cold
        'ma': lambda: draw.rectangle([60, 120, 140, 140], fill='black'),  # Ground/earth
        'sewi': lambda: [
            draw.polygon([(100, 60), (90, 80), (110, 80)], fill='black'),  # Up arrow
            draw.line([(100, 80), (100, 120)], fill='black', width=3)
        ],  # High/up
        'anpa': lambda: [
            draw.polygon([(100, 140), (90, 120), (110, 120)], fill='black'),  # Down arrow
            draw.line([(100, 80), (100, 120)], fill='black', width=3)
        ],  # Low/down
    }
    
    # Draw the shape if we have one, otherwise draw the word
    if word in geometric_shapes:
        result = geometric_shapes[word]()
        if result:  # Some shapes return a list
            pass  # Already drawn
    else:
        # Fallback: draw the word in a simple font with a geometric border
        try:
            font = ImageFont.load_default()
            # Calculate text position to center it
            bbox = draw.textbbox((0, 0), word, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            position = ((size[0] - text_width) / 2, (size[1] - text_height) / 2)
            
            # Draw a decorative border
            draw.rectangle([30, 30, size[0]-30, size[1]-30], outline='black', width=2)
            draw.text(position, word, font=font, fill='black')
        except:
            # Ultimate fallback: just draw a circle with the first letter
            draw.ellipse([50, 50, 150, 150], outline='black', width=3)
            draw.text((90, 90), word[0].upper(), fill='black')
    
    return img

def generate_sitelen_pona_image(word, font_path, output_dir, size=(200, 200)):
    """Generate an image for a sitelen pona character."""
    
    # Check if we have a valid sitelen pona font
    sitelen_pona_font_available = False
    if font_path and font_path.exists():
        # Check if this is actually a sitelen pona font, not just a fallback
        font_name = str(font_path).lower()
        if any(name in font_name for name in ['linja', 'pona', 'sitelen']) and font_name.endswith(('.ttf', '.otf')):
            sitelen_pona_font_available = True
        elif '/usr/share/fonts/' in font_name:  # Fallback system fonts should not be treated as Sitelen Pona fonts
            sitelen_pona_font_available = False
    
    if not sitelen_pona_font_available:
        print(f"No sitelen pona font available for '{word}', using geometric representation")
        img = generate_geometric_sitelen_pona(word, size)
    else:
        # Try to use the actual sitelen pona font
        img = Image.new('RGB', size, color='white')
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype(str(font_path), size=int(min(size) * 0.7))
            # Calculate text position to center it
            left, top, right, bottom = draw.textbbox((0, 0), word, font=font)
            text_width = right - left
            text_height = bottom - top
            position = ((size[0] - text_width) / 2, (size[1] - text_height) / 2)
            
            # Draw the text
            draw.text(position, word, font=font, fill='black')
        except Exception as e:
            print(f"Error loading sitelen pona font for '{word}', using geometric shapes: {e}")
            img = generate_geometric_sitelen_pona(word, size)
    
    # Save the image directly without additional border processing
    output_file = os.path.join(output_dir, f"{word}.png")
    img.save(output_file, 'PNG')
    
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
                # Make sure the image was created successfully
                if os.path.exists(image_path) and os.path.getsize(image_path) > 0:
                    print(f"✓ Generated image for '{word}': {os.path.basename(image_path)}")
                else:
                    print(f"✗ Failed to generate valid image for '{word}'")
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
            # Use just the basename for the image filename in notes
            image_path = word_to_image[word]
            if os.path.exists(image_path) and os.path.getsize(image_path) > 0:
                image_filename = os.path.basename(image_path)
                print(f"Using image for '{word}': {image_filename}")
            else:
                print(f"Warning: Image for '{word}' is invalid or empty")
        
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
        # For fonts, add the file with the original filename
        font_basename = os.path.basename(str(font_path))
        if font_basename.endswith(('.ttf', '.otf')):
            media_files.append(str(font_path))
            print(f"Adding font file to Anki package: {font_basename}")
        else:
            print(f"Font file doesn't have a valid extension (.ttf/.otf): {font_basename}")
    
    # Add all generated images to media files
    valid_image_files = []
    for word, path in word_to_image.items():
        if os.path.exists(path) and os.path.getsize(path) > 0:
            # For images, we need to make sure they're added with the same basename
            # that's referenced in the notes
            valid_image_files.append(str(path))
            print(f"Adding image file to Anki package: {os.path.basename(path)}")
    
    media_files.extend(valid_image_files)
    
    if media_files:
        anki_package.media_files = media_files
        print(f"Added {len(media_files)} media files to Anki package")
    
    anki_package.write_to_file(OUTPUT_FILE)
    print(f"Anki deck created: {OUTPUT_FILE}")
    print(f"Number of cards: {len(words_data) * 2}")  # Two card types per word
    
    # Add a helpful message about missing images
    print("\nNotes:")
    print("- If Sitelen Pona images aren't showing in Anki after importing the deck:")
    print("  1. In Anki, go to Tools > Check Media")
    print("  2. Close and restart Anki")
    print("  3. If that doesn't work, manually add the Sitelen Pona font to your system")
    print("     and update the card templates to use that font")

if __name__ == "__main__":
    create_anki_deck()