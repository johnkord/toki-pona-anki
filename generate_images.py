#!/usr/bin/env python3
"""
Script to generate sitelen pona images for all Toki Pona words.

This script generates images for all words in the toki_pona_words.json file
and saves them to the sitelen_pona_images directory.
"""

import json
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

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

def generate_all_images():
    """Generate images for all words in the JSON file."""
    # Load words data
    with open('toki_pona_words.json', 'r', encoding='utf-8') as f:
        words_data = json.load(f)
    
    # Create images directory
    images_dir = Path("sitelen_pona_images")
    images_dir.mkdir(exist_ok=True)
    
    print(f"Generating {len(words_data)} sitelen pona images...")
    
    # Generate images for all words
    for word in words_data.keys():
        try:
            img = generate_geometric_sitelen_pona(word, size=(200, 200))
            output_file = images_dir / f"{word}.png"
            img.save(output_file, 'PNG')
            
            if output_file.exists() and os.path.getsize(output_file) > 0:
                print(f"✓ Generated image for '{word}': {output_file.name}")
            else:
                print(f"✗ Failed to generate valid image for '{word}'")
                
        except Exception as e:
            print(f"Error generating image for '{word}': {e}")
    
    print(f"\nAll images generated in {images_dir}")
    print("These images can now be used by the Anki deck generator.")

if __name__ == "__main__":
    generate_all_images()