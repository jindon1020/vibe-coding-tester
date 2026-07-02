from __future__ import annotations

import re

from rag_app.domain.models import DocumentChunk, ScoredChunk


TOKEN_PATTERN = re.compile(r"[\w\u4e00-\u9fff]+", re.UNICODE)


class KeywordRetriever:
    def retrieve(self, query: str, chunks: list[DocumentChunk], top_k: int = 3) -> list[ScoredChunk]:
        """Return top_k chunks ranked by keyword matches.

        TODO: Candidate should implement this method.
        Expected behavior:
        - Tokenize query case-insensitively.
        - Score each chunk by matched keyword count.
        - Drop zero-score chunks.
        - Deduplicate identical chunk text.
        - Sort by score descending, then stable original order.
        """
        raise NotImplementedError


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_PATTERN.findall(text or "")]

