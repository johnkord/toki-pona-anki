# toki-pona-anki
An experiment to use GitHub Copilot Coding agent to generate a Toki Pona Anki deck using Sitelen Pona

## Overview

This repository contains a script to generate an Anki deck for learning Toki Pona using Sitelen Pona (the logographic writing system for Toki Pona). The deck includes all standard Toki Pona words with their definitions and their Sitelen Pona representations.

## Requirements

- Python 3.6 or higher
- Required Python packages: `genanki`, `requests`, `Pillow` (install using `pip install -r requirements.txt`)
- Internet connection (to download the Sitelen Pona font)
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

3. Run the script to generate the Anki deck:
   ```
   python generate_anki_deck.py
   ```

4. Import the generated `toki_pona_sitelen_pona.apkg` file into Anki.

## Deck Structure

The generated Anki deck contains two card types for each Toki Pona word:

1. **Sitelen Pona to Word + Definition**: Shows the Sitelen Pona character and image on the front and the word with its definition on the back.
2. **Word to Sitelen Pona + Definition**: Shows the Toki Pona word on the front and its Sitelen Pona character, image, and definition on the back.

## Notes

- The script attempts to automatically download a Sitelen Pona font, but if it fails, you'll need to:
  1. Download a Sitelen Pona font manually (e.g., from [Kreative Korp](https://www.kreativekorp.com/software/fonts/linjapona/))
  2. Place it in the `fonts` directory as `linjapona.otf`
  3. Install the font on your system
  4. In Anki, ensure the font is available for card templates
- The script generates both font-based Sitelen Pona characters and image versions of each character
- Images are embedded in the Anki deck to ensure they display correctly even without the font installed
- For proper display of Sitelen Pona characters in Anki, you may need to adjust the card templates to use the appropriate font.

## Credits

- Toki Pona language created by Sonja Lang
- linja pona font by jan Same
