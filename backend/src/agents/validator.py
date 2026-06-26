from __future__ import annotations

from pathlib import Path


def extract_evidence_text(file_path: str) -> str:
    suffix = Path(file_path).suffix.lower()
    if suffix in {".txt", ".md"}:
        return Path(file_path).read_text(encoding="utf-8")
    if suffix == ".pdf":
        from pypdf import PdfReader

        reader = PdfReader(file_path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if suffix == ".docx":
        from docx import Document

        doc = Document(file_path)
        return "\n".join(paragraph.text for paragraph in doc.paragraphs)
    raise ValueError("Unsupported evidence type")


def validate_evidence_against_map(map_requirement: str, evidence_text: str) -> dict:
    map_tokens = {token for token in map_requirement.lower().split() if len(token) > 3}
    evidence_lower = evidence_text.lower()
    matched_tokens = sum(1 for token in map_tokens if token in evidence_lower)
    confidence = min(100, 50 + matched_tokens * 10)
    verified = matched_tokens >= max(1, len(map_tokens) // 4)
    reasoning = (
        "Evidence contains the required compliance terminology and likely satisfies the MAP."
        if verified
        else "Evidence does not sufficiently match the MAP requirement."
    )
    return {"verified": verified, "confidence": confidence, "reasoning": reasoning}
