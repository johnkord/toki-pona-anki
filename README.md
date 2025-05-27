# toki-pona-anki
An experiment to use GitHub Copilot Coding agent to generate a Toki Pona Anki deck using Sitelen Pona

## Overview

This repository contains a script to generate an Anki deck for learning Toki Pona using Sitelen Pona (the logographic writing system for Toki Pona). The deck includes all standard Toki Pona words with their definitions and their Sitelen Pona representations.

## Requirements

- Python 3.6 or higher
- Required Python packages: `genanki`, `requests` (install using `pip install -r requirements.txt`)
- Internet connection (to download the Sitelen Pona font)
- Anki desktop application (to import the generated deck)

## Usage

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

1. **Sitelen Pona to Word + Definition**: Shows the Sitelen Pona character on the front and the word with its definition on the back.
2. **Word to Sitelen Pona + Definition**: Shows the Toki Pona word on the front and its Sitelen Pona character along with the definition on the back.

## Notes

- The script attempts to automatically download a Sitelen Pona font, but if it fails, you'll need to:
  1. Download a Sitelen Pona font manually (e.g., from [Kreative Korp](https://github.com/kreativekorp/linja-pona))
  2. Install the font on your system
  3. In Anki, ensure the font is available for card templates
- For proper display of Sitelen Pona characters in Anki, you may need to adjust the card templates to use the appropriate font.

## Credits

- Toki Pona language created by Sonja Lang
- linja pona font by jan Same
