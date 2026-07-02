from __future__ import annotations

from pathlib import Path

from rag_app.domain.models import DocumentChunk


class DocxLoader:
    def load(self, path: str | Path) -> list[DocumentChunk]:
        """Load non-empty paragraphs from a docx file.

        TODO: Candidate should implement this method.
        Expected behavior:
        - Read a .docx file.
        - Ignore empty paragraphs.
        - Return one DocumentChunk per paragraph.
        - Use stable chunk ids such as "<filename>#<index>".
        """
        raise NotImplementedError

