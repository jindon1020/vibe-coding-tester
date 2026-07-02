from __future__ import annotations

import re

from rag_app.domain.models import DocumentChunk, ScoredChunk


TOKEN_PATTERN = re.compile(r"[\w\u4e00-\u9fff]+", re.UNICODE)
CJK_TOKEN_PATTERN = re.compile(r"^[\u4e00-\u9fff]+$")


class KeywordRetriever:
    def retrieve(self, query: str, chunks: list[DocumentChunk], top_k: int = 3) -> list[ScoredChunk]:
        """Return top_k chunks ranked by keyword matches.

        Expected behavior:
        - Tokenize query case-insensitively.
        - Score each chunk by matched keyword count.
        - Drop zero-score chunks.
        - Deduplicate identical chunk text.
        - Sort by score descending, then stable original order.
        """
        query_tokens = tokenize(query)
        if not query_tokens:
            return []

        scored_chunks: list[ScoredChunk] = []
        seen_texts: set[str] = set()

        for chunk in chunks:
            if chunk.text in seen_texts:
                continue

            normalized_text = chunk.text.lower()
            score = sum(1 for token in query_tokens if token in normalized_text)
            if score <= 0:
                continue

            seen_texts.add(chunk.text)
            scored_chunks.append(ScoredChunk(chunk=chunk, score=score))

        scored_chunks.sort(key=lambda item: item.score, reverse=True)
        return scored_chunks[:top_k]


def tokenize(text: str) -> list[str]:
    normalized_tokens: list[str] = []

    for token in TOKEN_PATTERN.findall(text or ""):
        lowered = token.lower()
        if CJK_TOKEN_PATTERN.fullmatch(lowered) and len(lowered) > 2:
            normalized_tokens.extend(lowered[index : index + 2] for index in range(len(lowered) - 1))
            continue
        normalized_tokens.append(lowered)

    return normalized_tokens
