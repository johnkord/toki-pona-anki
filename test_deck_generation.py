#!/usr/bin/env python3
"""
Test script to verify the deck generation process
"""

import json
import tempfile
import os
from pathlib import Path
from generate_anki_deck import create_anki_deck, generate_sitelen_pona_images, download_font

def test_small_deck():
    """Create a small test deck with just a few words"""
    # Create a small test data set
    test_data = {
        "a": {"definition": "ah, ha, uh, oh, ooh, aw, well (emotion word)", "type": "particle"},
        "mi": {"definition": "I, me, we, us", "type": "pronoun"},
        "pona": {"definition": "good, positive, useful", "type": "adjective"}
    }
    
    # Save test data
    with open('test_words.json', 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    
    print("Created test words file")
    
    # Test font download
    font_path = download_font()
    print(f"Font path: {font_path}")
    
    if font_path and font_path.exists():
        # Test image generation
        word_to_image = generate_sitelen_pona_images(test_data, font_path)
        print(f"Generated {len(word_to_image)} images")
        
        for word, image_path in word_to_image.items():
            print(f"  {word}: {image_path} (exists: {os.path.exists(image_path)}, size: {os.path.getsize(image_path) if os.path.exists(image_path) else 'N/A'})")
    
    print("Test completed")

if __name__ == "__main__":
    test_small_deck()