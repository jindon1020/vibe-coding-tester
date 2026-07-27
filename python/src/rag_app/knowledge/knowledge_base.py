from __future__ import annotations

from pathlib import Path

from rag_app.document.docx_loader import DocxLoader
from rag_app.domain.models import DocumentChunk


class InMemoryKnowledgeBase:
    def __init__(self, loader: DocxLoader | None = None) -> None:
        self.loader = loader or DocxLoader()
        self._chunks: list[DocumentChunk] = []

    @property
    def chunks(self) -> list[DocumentChunk]:
        return list(self._chunks)

    def load_documents(self, paths: list[str | Path]) -> list[DocumentChunk]:
        """Load all docx files into memory and return stored chunks.

        Expected behavior:
        - Clear previous chunks before loading.
        - Load every path with DocxLoader.
        - Keep chunks in memory.
        """
        self._chunks.clear()
        loaded_chunks: list[DocumentChunk] = []
        for path in paths:
            loaded_chunks.extend(self.loader.load(path))

        self._chunks.extend(loaded_chunks)
        return self.chunks
