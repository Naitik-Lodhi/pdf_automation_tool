# pdf_utils.py

from PyPDF2 import PdfReader, PdfWriter, errors as pdf_errors
import os

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def merge_pdfs(paths, output_filename):
    writer = PdfWriter()
    try:
        for path in paths:
            try:
                reader = PdfReader(path)
            except Exception as e:
                raise ValueError(f"Failed to read PDF: {path}. Error: {e}")
            for page in reader.pages:
                writer.add_page(page)
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        with open(output_path, "wb") as f:
            writer.write(f)
        return output_path
    except Exception as e:
        raise RuntimeError(f"Failed to merge PDFs: {e}")

def split_pdf(path, start_page, end_page, output_filename):
    try:
        reader = PdfReader(path)
        writer = PdfWriter()
        num_pages = len(reader.pages)
        if start_page < 0 or end_page > num_pages or start_page >= end_page:
            raise ValueError(f"Invalid page range: {start_page} to {end_page} for file with {num_pages} pages.")
        for i in range(start_page, end_page):
            writer.add_page(reader.pages[i])
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        with open(output_path, "wb") as f:
            writer.write(f)
        return output_path
    except Exception as e:
        raise RuntimeError(f"Failed to split PDF: {e}")

def encrypt_pdf(path, password, output_filename):
    try:
        reader = PdfReader(path)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.encrypt(password)
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        with open(output_path, "wb") as f:
            writer.write(f)
        return output_path
    except Exception as e:
        raise RuntimeError(f"Failed to encrypt PDF: {e}")
