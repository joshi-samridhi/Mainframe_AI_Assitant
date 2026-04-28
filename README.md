# Mainframe Error Screen Image Generator

This project generates annotated mainframe terminal screen images for common error codes used in training and documentation.

## Generated Error Screens

The following error screens are included:

1. **U0777** - Data Validation Abend
2. **S013** - Dataset Open Error (DCB/RECFM Mismatch)
3. **S0C7** - Numeric Data Exception

Each image features:
- Dark terminal background with green text (authentic mainframe style)
- Red boxes highlighting error codes and failing steps
- Circles and arrows pointing to problem areas
- Clear error labels
- Green "Resolution Checklist" box with step-by-step guidance

## Prerequisites

Before running the generator, you need:

- **Python 3.7 or higher** installed on your system
- **Pillow (PIL)** library for image generation

## Installation

### Step 1: Install Python

If Python is not installed on your system:

**Windows:**
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **Important:** Check "Add Python to PATH" during installation
4. Verify installation: Open Command Prompt and run `python --version`

**Alternative (Windows):**
- Install from Microsoft Store: Search for "Python" in the Microsoft Store

### Step 2: Install Dependencies

Open a terminal/command prompt in the `mainframe-error-screens` directory and run:

```bash
python -m pip install -r requirements.txt
```

Or install Pillow directly:

```bash
python -m pip install Pillow
```

## Usage

### Generate All Error Screens

Run the main script to generate all three error screen images:

```bash
python generate_error_screens.py
```

This will create three PNG images in the `output/` directory:
- `U0777_error_screen.png`
- `S013_error_screen.png`
- `S0C7_error_screen.png`

### Output Location

All generated images are saved in:
```
mainframe-error-screens/output/
```

## Error Screen Details

### U0777 - Data Validation Abend

**Scenario:** Job fails due to invalid data in a record

**Visual Elements:**
- Red box around "U0777" return code
- Red highlight on "STEP002"
- Circle around "RECORD#007"
- Arrow pointing to the offending record
- Label: "U0777 - Data validation abend"

**Resolution Checklist:**
1. Isolate RECORD#007
2. Check copybook format
3. Fix invalid data
4. Re-run STEP002

---

### S013 - Dataset Open Error

**Scenario:** Job fails due to dataset attribute mismatch (RECFM/LRECL)

**Visual Elements:**
- Red box around "S013" return code
- Red highlight on "STEP005"
- Yellow highlight on "DDNAME INPUT1"
- Circle around "RECFM or LRECL incorrect"
- Arrow pointing to the dataset issue
- Label: "S013 - Dataset open error"

**Resolution Checklist:**
1. Check DD statement in JCL
2. Verify RECFM and LRECL
3. Compare with dataset attributes
4. Correct JCL and re-run job

---

### S0C7 - Numeric Data Exception

**Scenario:** Job fails due to invalid numeric data in a field

**Visual Elements:**
- Red box around "S0C7" return code
- Red highlight on "STEP010"
- Circle around field "AMOUNT"
- Arrow pointing to the invalid numeric value
- Label: "S0C7 - Numeric data exception"

**Resolution Checklist:**
1. Check numeric fields
2. Remove invalid characters
3. Validate input data
4. Re-run job

## Customization

To modify the generated images, edit `generate_error_screens.py`:

- **Colors:** Modify color constants at the top of the file
- **Dimensions:** Change `WIDTH` and `HEIGHT` variables
- **Font sizes:** Adjust `get_font(size)` calls
- **Content:** Edit the text and positioning in each generator function

## Image Specifications

- **Format:** PNG
- **Dimensions:** 1400 x 900 pixels
- **Background:** Dark terminal (#0a0a0a)
- **Text Color:** Green (#00ff00)
- **Error Highlights:** Red (#ff0000)
- **Annotations:** Yellow (#ffff00) and White (#ffffff)

## Use Cases

These images are ideal for:
- Mainframe training materials
- Technical documentation
- Error handling guides
- Troubleshooting manuals
- Educational presentations
- Wiki pages and knowledge bases

## Troubleshooting

### Python not found
- Ensure Python is installed and added to your system PATH
- Try using `python3` instead of `python` on some systems
- On Windows, you may need to use `py` command

### Pillow installation fails
- Try upgrading pip first: `python -m pip install --upgrade pip`
- Then retry: `python -m pip install Pillow`

### Font issues
The script attempts to use Courier font for authentic terminal appearance. If unavailable, it falls back to the default system font.

## Project Structure

```
mainframe-error-screens/
├── generate_error_screens.py    # Main image generator script
├── requirements.txt              # Python dependencies
├── README.md                     # This file
└── output/                       # Generated images directory
    ├── U0777_error_screen.png
    ├── S013_error_screen.png
    └── S0C7_error_screen.png
```

## License

This project is provided as-is for educational and training purposes.

## Support

For issues or questions about the generated images, please refer to the inline comments in `generate_error_screens.py` or modify the script to suit your specific needs.

---

**Note:** These are simulated mainframe error screens for training purposes. Actual mainframe error messages may vary depending on your system configuration and software versions.