# toki-pona-anki
An experiment to use GitHub Copilot Coding agent to generate a Toki Pona Anki deck using Sitelen Pona

## Overview

This repository contains a script to generate an Anki deck for learning Toki Pona using Sitelen Pona (the logographic writing system for Toki Pona). The deck includes all standard Toki Pona words with their definitions and their Sitelen Pona representations.

## Requirements

- Python 3.6 or higher
- Required Python packages: `genanki`, `Pillow` (install using `pip install -r requirements.txt`)
- `nasin-nanpa-4.0.2-UCSUR.otf` font file (should be included in the repository)
- Anki desktop application (to import the generated deck)

## Usage

### Option 1: Download the pre-built deck

The latest version of the Anki deck is automatically built and released whenever changes are merged to the main branch. Each release is tagged with a date and time stamp (format: YYYY.MM.DD-HH.MM.SS). You can download the most recent deck from the [Releases](https://github.com/johnkord/toki-pona-anki/releases) page.

### Option 2: Build the deck yourself

1. Clone this repository:
   ```
   git clone https://github.com/johnkord/toki-pona-anki.git
   cd toki-pona-anki
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Generate the Sitelen Pona images (if not already present):
   ```
   python generate_images.py
   ```

4. Run the script to generate the Anki deck:
   ```
   python generate_anki_deck.py
   ```

5. Import the generated `toki_pona_sitelen_pona.apkg` file into Anki.

## Deck Structure

The generated Anki deck contains four card types for each Toki Pona word:

1. **Word to Sitelen Pona + Definition**: Shows the Toki Pona word on the front and its Sitelen Pona character, image, and definition on the back.
2. **Definition to Word + Sitelen Pona**: Shows the definition on the front and you have to guess the word and Sitelen Pona representation on the back.
3. **Image to Word + Definition**: Shows only the Sitelen Pona image on the front and you have to guess the word and its definition on the back.
4. **Word to Definition + Image**: Shows the Toki Pona word on the front and you have to guess the definition and Sitelen Pona image on the back.

These card variants ensure comprehensive learning from different angles while maintaining the constraint that no card shows both the word and image together on the front side.

## Sitelen Pona Image Generation

The deck uses authentic Sitelen Pona hieroglyphic images generated using the nasin nanpa font with proper Unicode character mappings (UCSUR F1900-F19FF). 

To generate the images:
1. Ensure `nasin-nanpa-4.0.2-UCSUR.otf` is in the repository root
2. Run `python generate_images.py`

The script will:
- Use the nasin nanpa font with proper Unicode codepoints for authentic sitelen pona characters
- Fall back to placeholder images if the font is not available
- Generate optimized 200x200 PNG images for all 137 Toki Pona words
- Optimize images for web compatibility (including AnkiApp support)

## Notes

- All Sitelen Pona images use authentic Unicode character mappings from the official UCSUR standard
- Images are pre-generated and embedded in the Anki deck for consistent display
- Images are optimized for web compatibility, ensuring they work in both Anki desktop and AnkiApp
- The nasin nanpa font provides the most accurate Sitelen Pona representations
- If images appear as squares with X's, the Unicode font approach failed and placeholders were used

## Troubleshooting

### Images not showing in cards

If the Sitelen Pona images aren't showing in your Anki cards after importing the deck:

1. In Anki, go to **Tools > Check Media** to ensure all media files are properly recognized
2. Close and restart Anki to refresh the media cache
3. If that doesn't work, try the following:
   - Make sure you have a Sitelen Pona font installed on your system
   - In Anki, edit the card template to ensure the `<img>` tags are properly formatted
   - Look for any error messages in Anki's browser console (Ctrl+Shift+I or Cmd+Option+I on Mac)

### Images showing as broken in AnkiApp (Web App)

If images appear as broken or don't load in AnkiApp but work fine in Anki desktop:

1. This has been fixed in recent versions - try downloading the latest deck from the releases page
2. The images are now optimized for web compatibility with better compression and HTML attributes
3. If you're building the deck yourself, make sure to regenerate both images and the deck:
   ```
   python generate_images.py
   python generate_anki_deck.py
   ```

### Missing or incorrect Sitelen Pona images

If the Sitelen Pona images are showing as squares with X's or generic placeholders:

1. Ensure `nasin-nanpa-4.0.2-UCSUR.otf` is in the repository root directory
2. Regenerate the images by running:
   ```
   python generate_images.py
   ```
3. Regenerate the Anki deck:
   ```
   python generate_anki_deck.py
   ```
4. Re-import the deck into Anki

### Font not available

If the nasin nanpa font is not available, the script will generate placeholder images with the word names. To get authentic sitelen pona hieroglyphs:

1. Obtain the `nasin-nanpa-4.0.2-UCSUR.otf` font file
2. Place it in the repository root directory
3. Regenerate images and deck as described above

## Credits

- Toki Pona language created by Sonja Lang
- nasin nanpa font by jan Same
- Unicode sitelen pona character mappings from UCSUR (F1900-F19FF)
