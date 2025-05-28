#!/usr/bin/env python3
"""
Test script to verify the Anki package structure
"""

import json
import os
import genanki
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw

# Simple test with minimal deck
def create_test_deck():
    """Create a minimal test deck to verify image embedding"""
    
    # Create a simple test image
    img = Image.new('RGB', (100, 100), color='red')
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), "TEST", fill='white')
    
    test_image_path = Path("test_simple.png")
    img.save(test_image_path)
    print(f"Created test image: {test_image_path}")
    
    # Create Anki model
    model = genanki.Model(
        1607392319,
        'Simple Test Model',
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
            {'name': 'Image'}
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Question}}<br><img src="{{Image}}">',
                'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
            },
        ])
    
    # Create deck
    deck = genanki.Deck(
        2059400110,
        'Test Deck')
    
    # Add a note
    note = genanki.Note(
        model=model,
        fields=['What is this?', 'A test image', 'test_simple.png'])
    deck.add_note(note)
    
    # Create package with media
    package = genanki.Package(deck)
    package.media_files = [str(test_image_path)]
    
    # Write to file
    package.write_to_file('test_deck.apkg')
    print("Created test_deck.apkg")
    
    # Clean up
    test_image_path.unlink()
    
    return True

if __name__ == "__main__":
    create_test_deck()