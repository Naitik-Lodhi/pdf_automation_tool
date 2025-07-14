# PDF Automation GUI Tool

A user-friendly desktop application for automating common PDF tasks such as merging, splitting, and encrypting PDF files. Built with Python, Tkinter, and PyPDF2.

## Features
- Merge multiple PDF files into one
- Split a PDF by page range
- Encrypt a PDF with a password
- All outputs saved to a dedicated `output/` directory
- Simple, modern GUI

## Planned Features
- Drag-and-drop file support
- Open output directory button
- Recent files list
- Progress bar for long operations
- PDF page preview before splitting
- Rotate and extract pages
- Remove password from encrypted PDFs
- Batch processing for splitting/encrypting
- Logging and improved error handling

## Installation
1. Clone this repository:
   ```bash
   git clone <repo-url>
   cd pdf_automation_gui_tool
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Or manually:
   ```bash
   pip install PyPDF2
   ```
   (Tkinter is included with most Python installations.)

## Usage
Run the application:
```bash
python app.py
```

- Use the GUI to select and process PDF files.
- All output files are saved in the `output/` directory.

## Dependencies
- Python 3.7+
- PyPDF2
- Tkinter (usually included with Python)

## License
MIT
