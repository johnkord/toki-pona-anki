#!/usr/bin/env python3
"""
Sitelen Pona Unicode mappings and alternative image generation
"""

# Unicode sitelen pona mappings (Private Use Area U+F1900-F19FF)
# This is based on the UCSUR (Under ConScript Unicode Registry) standard
SITELEN_PONA_UNICODE = {
    'a': '\U000F1900',
    'akesi': '\uF1901', 
    'ala': '\uF1902',
    'alasa': '\uF1903',
    'ale': '\uF1904',
    'ali': '\uF1904',  # Same as ale
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
    'oko': '\uF1945',
    'olin': '\uF1946',
    'ona': '\uF1947',
    'open': '\uF1948',
    'pakala': '\uF1949',
    'pali': '\uF194A',
    'palisa': '\uF194B',
    'pan': '\uF194C',
    'pana': '\uF194D',
    'pi': '\uF194E',
    'pilin': '\uF194F',
    'pimeja': '\uF1950',
    'pini': '\uF1951',
    'pipi': '\uF1952',
    'poka': '\uF1953',
    'poki': '\uF1954',
    'pona': '\uF1955',
    'pu': '\uF1956',
    'sama': '\uF1957',
    'seli': '\uF1958',
    'selo': '\uF1959',
    'seme': '\uF195A',
    'sewi': '\uF195B',
    'sijelo': '\uF195C',
    'sike': '\uF195D',
    'sin': '\uF195E',
    'sina': '\uF195F',
    'sinpin': '\uF1960',
    'sitelen': '\uF1961',
    'sona': '\uF1962',
    'soweli': '\uF1963',
    'suli': '\uF1964',
    'suno': '\uF1965',
    'supa': '\uF1966',
    'suwi': '\uF1967',
    'tan': '\uF1968',
    'taso': '\uF1969',
    'tawa': '\uF196A',
    'telo': '\uF196B',
    'tenpo': '\uF196C',
    'toki': '\uF196D',
    'tomo': '\uF196E',
    'tu': '\uF196F',
    'unpa': '\uF1970',
    'uta': '\uF1971',
    'utala': '\uF1972',
    'walo': '\uF1973',
    'wan': '\uF1974',
    'waso': '\uF1975',
    'wawa': '\uF1976',
    'weka': '\uF1977',
    'wile': '\uF1978'
}

def test_unicode_sitelen_pona():
    """Test if Unicode sitelen pona characters work"""
    from PIL import Image, ImageDraw, ImageFont
    
    # Test a few characters
    test_words = ['a', 'mi', 'pona']
    
    for word in test_words:
        if word in SITELEN_PONA_UNICODE:
            unicode_char = SITELEN_PONA_UNICODE[word]
            print(f"{word}: {unicode_char} (Unicode: U+{ord(unicode_char):04X})")
            
            # Try to create an image with this character
            img = Image.new('RGB', (200, 200), color='white')
            draw = ImageDraw.Draw(img)
            
            # Try with system fonts that might support sitelen pona
            fonts_to_try = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
            ]
            
            for font_path in fonts_to_try:
                try:
                    font = ImageFont.truetype(font_path, 100)
                    draw.text((50, 50), unicode_char, font=font, fill='black')
                    img.save(f'unicode_test_{word}.png')
                    print(f"  Created unicode_test_{word}.png with font {font_path}")
                    break
                except Exception as e:
                    print(f"  Failed with font {font_path}: {e}")

if __name__ == "__main__":
    test_unicode_sitelen_pona()