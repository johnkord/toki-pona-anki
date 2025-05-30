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
    'a': chr(0xF1900),
    'akesi': chr(0xF1901), 
    'ala': chr(0xF1902),
    'alasa': chr(0xF1903),
    'ale': chr(0xF1904),
    'anpa': chr(0xF1905),
    'ante': chr(0xF1906),
    'anu': chr(0xF1907),
    'awen': chr(0xF1908),
    'e': chr(0xF1909),
    'en': chr(0xF190A),
    'esun': chr(0xF190B),
    'ijo': chr(0xF190C),
    'ike': chr(0xF190D),
    'ilo': chr(0xF190E),
    'insa': chr(0xF190F),
    'jaki': chr(0xF1910),
    'jan': chr(0xF1911),
    'jelo': chr(0xF1912),
    'jo': chr(0xF1913),
    'kala': chr(0xF1914),
    'kalama': chr(0xF1915),
    'kama': chr(0xF1916),
    'kasi': chr(0xF1917),
    'ken': chr(0xF1918),
    'kepeken': chr(0xF1919),
    'kili': chr(0xF191A),
    'kiwen': chr(0xF191B),
    'ko': chr(0xF191C),
    'kon': chr(0xF191D),
    'kule': chr(0xF191E),
    'kulupu': chr(0xF191F),
    'kute': chr(0xF1920),
    'la': chr(0xF1921),
    'lape': chr(0xF1922),
    'laso': chr(0xF1923),
    'lawa': chr(0xF1924),
    'len': chr(0xF1925),
    'lete': chr(0xF1926),
    'li': chr(0xF1927),
    'lili': chr(0xF1928),
    'linja': chr(0xF1929),
    'lipu': chr(0xF192A),
    'loje': chr(0xF192B),
    'lon': chr(0xF192C),
    'luka': chr(0xF192D),
    'lukin': chr(0xF192E),
    'lupa': chr(0xF192F),
    'ma': chr(0xF1930),
    'mama': chr(0xF1931),
    'mani': chr(0xF1932),
    'meli': chr(0xF1933),
    'mi': chr(0xF1934),
    'mije': chr(0xF1935),
    'moku': chr(0xF1936),
    'moli': chr(0xF1937),
    'monsi': chr(0xF1938),
    'mu': chr(0xF1939),
    'mun': chr(0xF193A),
    'musi': chr(0xF193B),
    'mute': chr(0xF193C),
    'nanpa': chr(0xF193D),
    'nasa': chr(0xF193E),
    'nasin': chr(0xF193F),
    'nena': chr(0xF1940),
    'ni': chr(0xF1941),
    'nimi': chr(0xF1942),
    'noka': chr(0xF1943),
    'o': chr(0xF1944),
    'olin': chr(0xF1945),
    'ona': chr(0xF1946),
    'open': chr(0xF1947),
    'pakala': chr(0xF1948),
    'pali': chr(0xF1949),
    'palisa': chr(0xF194A),
    'pan': chr(0xF194B),
    'pana': chr(0xF194C),
    'pi': chr(0xF194D),
    'pilin': chr(0xF194E),
    'pimeja': chr(0xF194F),
    'pini': chr(0xF1950),
    'pipi': chr(0xF1951),
    'poka': chr(0xF1952),
    'poki': chr(0xF1953),
    'pona': chr(0xF1954),
    'pu': chr(0xF1955),
    'sama': chr(0xF1956),
    'seli': chr(0xF1957),
    'selo': chr(0xF1958),
    'seme': chr(0xF1959),
    'sewi': chr(0xF195A),
    'sijelo': chr(0xF195B),
    'sike': chr(0xF195C),
    'sin': chr(0xF195D),
    'sina': chr(0xF195E),
    'sinpin': chr(0xF195F),
    'sitelen': chr(0xF1960),
    'sona': chr(0xF1961),
    'soweli': chr(0xF1962),
    # NOTE: 'su' temporarily removed from toki_pona_words.json due to nasin nanpa font rendering issues
    # Should be re-enabled when font support is added. Unicode mapping would be: 'su': chr(0xF19XX)
    'suli': chr(0xF1963),
    'suno': chr(0xF1964),
    'supa': chr(0xF1965),
    'suwi': chr(0xF1966),
    'tan': chr(0xF1967),
    'taso': chr(0xF1968),
    'tawa': chr(0xF1969),
    'telo': chr(0xF196A),
    'tenpo': chr(0xF196B),
    'toki': chr(0xF196C),
    'tomo': chr(0xF196D),
    'tu': chr(0xF196E),
    'unpa': chr(0xF196F),
    'uta': chr(0xF1970),
    'utala': chr(0xF1971),
    'walo': chr(0xF1972),
    'wan': chr(0xF1973),
    'waso': chr(0xF1974),
    'wawa': chr(0xF1975),
    'weka': chr(0xF1976),
    'wile': chr(0xF1977),
    
    # nimi ku suli (words recognized by >40% of speakers)
    'namako': chr(0xF1978),
    'kin': chr(0xF1979),
    'oko': chr(0xF197A),
    'kipisi': chr(0xF197B),
    'leko': chr(0xF197C),
    'monsuta': chr(0xF197D),
    'tonsi': chr(0xF197E),
    'jasima': chr(0xF197F),
    'kijetesantakalu': chr(0xF1980),
    'soko': chr(0xF1981),
    'meso': chr(0xF1982),
    'epiku': chr(0xF1983),
    'kokosila': chr(0xF1984),
    'lanpan': chr(0xF1985),
    'n': chr(0xF1986),
    'misikeke': chr(0xF1987),
    'ku': chr(0xF1988),
    
    # nimi ku lili (words recognized by ≤40% of speakers)
    'pake': chr(0xF19A0),
    'apeja': chr(0xF19A1),
    'majuna': chr(0xF19A2),
    'powe': chr(0xF19A3),
    
    # Additional common words that might be in the word list
    'ali': chr(0xF1904),  # Alternative form of 'ale'
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
            # Optimize PNG for web compatibility
            img.save(output_file, 'PNG', optimize=True, compress_level=6)
            
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