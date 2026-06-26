from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader


def extract_pdf_text(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    extracted = []
    for page in reader.pages:
        extracted.append(page.extract_text() or "")
    return clean_text("\n".join(extracted))


def clean_text(text: str) -> str:
    return " ".join(text.replace("\x00", " ").split())


def ensure_storage_path(file_name: str) -> Path:
    storage_dir = Path("uploads")
    storage_dir.mkdir(exist_ok=True)
    return storage_dir / file_name
