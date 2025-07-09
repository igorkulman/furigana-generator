# furigana-generator

Simple Python script that adds furigana to Japanese text.

It generates a clean, printable HTML output from a text file. It uses [SudachiPy](https://github.com/WorksApplications/SudachiPy) for high-quality tokenization.

## Usage

Install dependencies

```bash
pip install -r requirements.txt
```

Place your Japanese text into a `.txt` file (UTF-8 encoded).

### Basic Usage

To generate furigana for all kanji in your text:

```bash
python furigana_generator.py input.txt
```

This will create an `input.html` file in the same directory.

### Ignoring Kanji by Level

You can specify a Kanji proficiency level (e.g., N5, N4) to ignore kanji at or below that level. Furigana will not be added to kanji that are part of the specified level's set. If no level is specified, furigana will be applied to all kanji.

Use the `-k` or `--kanji-level` option:

*   **Ignore N5 Kanji:**
    ```bash
    python furigana_generator.py -k N5 input.txt
    ```
    (Furigana will not be added to N5 level kanji.)

*   **Ignore N4 Kanji (includes N5):**
    ```bash
    python furigana_generator.py -k N4 input.txt
    ```
    (Furigana will not be added to N4 or N5 level kanji.)

*   **Ignore N3 Kanji (includes N4 and N5):**
    ```bash
    python furigana_generator.py -k N3 input.txt
    ```
    (Furigana will not be added to N3, N4, or N5 level kanji.)

*   **Ignore N2 Kanji (includes N3, N4 and N5):**
    ```bash
    python furigana_generator.py -k N2 input.txt
    ```
    (Furigana will not be added to N2, N3, N4, or N5 level kanji.)

*   **Ignore All Kanji (N1):**
    ```bash
    python furigana_generator.py -k N1 input.txt
    ```
    (Furigana will not be added to any kanji, effectively ignoring all kanji.)

## License

MIT
