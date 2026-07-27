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
        document_path = Path(path)
        if document_path.suffix.lower() != ".docx":
            raise ValueError(f"Expected a .docx file: {document_path}")
        if not document_path.is_file():
            raise FileNotFoundError(f"Document does not exist: {document_path}")

        document = Document(str(document_path))
        chunks: list[DocumentChunk] = []
        for paragraph in document.paragraphs:
            text = paragraph.text.strip()
            if not text:
                continue
            chunk_index = len(chunks)
            chunks.append(
                DocumentChunk(
                    id=f"{document_path.name}#{chunk_index}",
                    source=document_path.name,
                    text=text,
                )
            )
        return chunks
