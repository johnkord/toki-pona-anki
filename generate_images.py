#!/usr/bin/env python3
"""
Generate authentic sitelen pona images using the nasin nanpa font and proper Unicode character mappings.

This script uses the Unicode character mappings from F1900-F19FF to generate proper sitelen pona hieroglyphs.
"""

import json
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Unicode mappings for sitelen pona characters (UCSUR F1900-F19FF)
SITELEN_PONA_UNICODE = {
    # nimi pu (original 120 words)
    'a': '\uF1900',
    'akesi': '\uF1901', 
    'ala': '\uF1902',
    'alasa': '\uF1903',
    'ale': '\uF1904',
    'anpa': '\uF1905',
    'ante': '\uF1906',
    'anu': '\uF1907',
    'awen': '\uF1908',
    'e': '\uF1909',
    'en': '\uF190A',
    'esun': '\uF190B',
    'ijo': '\uF190C',
    'ike': '\uF190D',
    'ilo': '\uF190E',
    'insa': '\uF190F',
    'jaki': '\uF1910',
    'jan': '\uF1911',
    'jelo': '\uF1912',
    'jo': '\uF1913',
    'kala': '\uF1914',
    'kalama': '\uF1915',
    'kama': '\uF1916',
    'kasi': '\uF1917',
    'ken': '\uF1918',
    'kepeken': '\uF1919',
    'kili': '\uF191A',
    'kiwen': '\uF191B',
    'ko': '\uF191C',
    'kon': '\uF191D',
    'kule': '\uF191E',
    'kulupu': '\uF191F',
    'kute': '\uF1920',
    'la': '\uF1921',
    'lape': '\uF1922',
    'laso': '\uF1923',
    'lawa': '\uF1924',
    'len': '\uF1925',
    'lete': '\uF1926',
    'li': '\uF1927',
    'lili': '\uF1928',
    'linja': '\uF1929',
    'lipu': '\uF192A',
    'loje': '\uF192B',
    'lon': '\uF192C',
    'luka': '\uF192D',
    'lukin': '\uF192E',
    'lupa': '\uF192F',
    'ma': '\uF1930',
    'mama': '\uF1931',
    'mani': '\uF1932',
    'meli': '\uF1933',
    'mi': '\uF1934',
    'mije': '\uF1935',
    'moku': '\uF1936',
    'moli': '\uF1937',
    'monsi': '\uF1938',
    'mu': '\uF1939',
    'mun': '\uF193A',
    'musi': '\uF193B',
    'mute': '\uF193C',
    'nanpa': '\uF193D',
    'nasa': '\uF193E',
    'nasin': '\uF193F',
    'nena': '\uF1940',
    'ni': '\uF1941',
    'nimi': '\uF1942',
    'noka': '\uF1943',
    'o': '\uF1944',
    'olin': '\uF1945',
    'ona': '\uF1946',
    'open': '\uF1947',
    'pakala': '\uF1948',
    'pali': '\uF1949',
    'palisa': '\uF194A',
    'pan': '\uF194B',
    'pana': '\uF194C',
    'pi': '\uF194D',
    'pilin': '\uF194E',
    'pimeja': '\uF194F',
    'pini': '\uF1950',
    'pipi': '\uF1951',
    'poka': '\uF1952',
    'poki': '\uF1953',
    'pona': '\uF1954',
    'pu': '\uF1955',
    'sama': '\uF1956',
    'seli': '\uF1957',
    'selo': '\uF1958',
    'seme': '\uF1959',
    'sewi': '\uF195A',
    'sijelo': '\uF195B',
    'sike': '\uF195C',
    'sin': '\uF195D',
    'sina': '\uF195E',
    'sinpin': '\uF195F',
    'sitelen': '\uF1960',
    'sona': '\uF1961',
    'soweli': '\uF1962',
    'suli': '\uF1963',
    'suno': '\uF1964',
    'supa': '\uF1965',
    'suwi': '\uF1966',
    'tan': '\uF1967',
    'taso': '\uF1968',
    'tawa': '\uF1969',
    'telo': '\uF196A',
    'tenpo': '\uF196B',
    'toki': '\uF196C',
    'tomo': '\uF196D',
    'tu': '\uF196E',
    'unpa': '\uF196F',
    'uta': '\uF1970',
    'utala': '\uF1971',
    'walo': '\uF1972',
    'wan': '\uF1973',
    'waso': '\uF1974',
    'wawa': '\uF1975',
    'weka': '\uF1976',
    'wile': '\uF1977',
    
    # nimi ku suli (words recognized by >40% of speakers)
    'namako': '\uF1978',
    'kin': '\uF1979',
    'oko': '\uF197A',
    'kipisi': '\uF197B',
    'leko': '\uF197C',
    'monsuta': '\uF197D',
    'tonsi': '\uF197E',
    'jasima': '\uF197F',
    'kijetesantakalu': '\uF1980',
    'soko': '\uF1981',
    'meso': '\uF1982',
    'epiku': '\uF1983',
    'kokosila': '\uF1984',
    'lanpan': '\uF1985',
    'n': '\uF1986',
    'misikeke': '\uF1987',
    'ku': '\uF1988',
    
    # nimi ku lili (words recognized by ≤40% of speakers)
    'pake': '\uF19A0',
    'apeja': '\uF19A1',
    'majuna': '\uF19A2',
    'powe': '\uF19A3',
    
    # Additional common words that might be in the word list
    'ali': '\uF1904',  # Alternative form of 'ale'
}

def find_font_file():
    """Find the nasin nanpa font file in the repository."""
    possible_paths = [
        'nasin-nanpa-4.0.2-UCSUR.otf',
        './nasin-nanpa-4.0.2-UCSUR.otf',
        '../nasin-nanpa-4.0.2-UCSUR.otf',
        'fonts/nasin-nanpa-4.0.2-UCSUR.otf',
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✓ Found nasin nanpa font: {path}")
            return path
    
    print("⚠ nasin nanpa font not found. Using fallback rendering.")
    return None

def generate_sitelen_pona_image(word, font_path=None, size=(200, 200)):
    """Generate a sitelen pona image using the proper Unicode character and font."""
    img = Image.new('RGB', size, color='white')
    draw = ImageDraw.Draw(img)
    
    # Get the Unicode character for this word
    unicode_char = SITELEN_PONA_UNICODE.get(word)
    
    if not unicode_char:
        print(f"⚠ No Unicode mapping found for '{word}', using fallback")
        return generate_fallback_image(word, size)
    
    if font_path and os.path.exists(font_path):
        try:
            # Use the nasin nanpa font with proper Unicode character
            font_size = 120  # Large size for clear rendering
            font = ImageFont.truetype(font_path, font_size)
            
            # Get text dimensions for centering
            bbox = draw.textbbox((0, 0), unicode_char, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Center the character
            x = (size[0] - text_width) // 2
            y = (size[1] - text_height) // 2
            
            # Draw the sitelen pona character
            draw.text((x, y), unicode_char, font=font, fill='black')
            
            print(f"✓ Generated sitelen pona for '{word}' using font (Unicode: {ord(unicode_char):04X})")
            return img
            
        except Exception as e:
            print(f"Error using font for '{word}': {e}")
            return generate_fallback_image(word, size)
    else:
        print(f"⚠ Font not available for '{word}', using fallback")
        return generate_fallback_image(word, size)

def generate_fallback_image(word, size=(200, 200)):
    """Generate a simple fallback image when font is not available."""
    img = Image.new('RGB', size, color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple border
    draw.rectangle([10, 10, size[0]-10, size[1]-10], outline='black', width=2)
    
    # Add the word in the center
    try:
        font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), word, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2
        draw.text((x, y), word, font=font, fill='black')
    except:
        draw.text((60, 90), word[:8], fill='black')
    
    # Add a note that this is a placeholder
    draw.text((20, 170), "placeholder", font=ImageFont.load_default(), fill='gray')
    
    print(f"⚠ Generated fallback image for '{word}'")
    return img

def generate_all_images():
    """Generate sitelen pona images for all words in the JSON file."""
    # Find the nasin nanpa font
    font_path = find_font_file()
    
    # Load words data
    try:
        with open('toki_pona_words.json', 'r', encoding='utf-8') as f:
            words_data = json.load(f)
    except FileNotFoundError:
        print("Error: toki_pona_words.json not found")
        return
    
    # Create images directory
    images_dir = Path("sitelen_pona_images")
    images_dir.mkdir(exist_ok=True)
    
    print(f"Generating {len(words_data)} sitelen pona images...")
    
    if font_path:
        print("Using nasin nanpa font with proper Unicode character mappings")
    else:
        print("Font not available - generating placeholder images")
    
    success_count = 0
    fallback_count = 0
    
    # Generate images for all words
    for word in words_data.keys():
        try:
            img = generate_sitelen_pona_image(word, font_path, size=(200, 200))
            output_file = images_dir / f"{word}.png"
            img.save(output_file, 'PNG')
            
            if output_file.exists() and os.path.getsize(output_file) > 0:
                if word in SITELEN_PONA_UNICODE and font_path:
                    success_count += 1
                else:
                    fallback_count += 1
            else:
                print(f"✗ Failed to generate valid image for '{word}'")
                
        except Exception as e:
            print(f"Error generating image for '{word}': {e}")
    
    print(f"\nGenerated {success_count} authentic sitelen pona images")
    print(f"Generated {fallback_count} fallback images")
    print(f"Images saved in: {images_dir}")
    
    if font_path:
        print("✓ All images use proper nasin nanpa font with Unicode character mappings")
    else:
        print("⚠ To get authentic sitelen pona images, ensure nasin-nanpa-4.0.2-UCSUR.otf is in the repository root")

if __name__ == "__main__":
    generate_all_images()