from __future__ import annotations

from pathlib import Path

from docx import Document

from rag_app.domain.models import DocumentChunk


class DocxLoader:
    def load(self, path: str | Path) -> list[DocumentChunk]:
        """Load non-empty paragraphs from a docx file.

        Expected behavior:
        - Read a .docx file.
        - Ignore empty paragraphs.
        - Return one DocumentChunk per paragraph.
        - Use stable chunk ids such as "<filename>#<index>".
        """
        docx_path = Path(path)
        document = Document(docx_path)
        chunks: list[DocumentChunk] = []

        for index, paragraph in enumerate(document.paragraphs):
            text = paragraph.text.strip()
            if not text:
                continue

            chunk_id = f"{docx_path.name}#{index}"
            chunks.append(DocumentChunk(id=chunk_id, source=str(docx_path), text=text))

        return chunks
