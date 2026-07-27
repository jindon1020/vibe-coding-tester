from __future__ import annotations

import re

from rag_app.domain.models import DocumentChunk, ScoredChunk


TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9_]+|[\u4e00-\u9fff]+", re.UNICODE)


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
        if top_k <= 0:
            return []

        keywords = list(dict.fromkeys(tokenize(query)))
        if not keywords:
            return []

        scored_chunks: list[ScoredChunk] = []
        seen_texts: set[str] = set()
        for chunk in chunks:
            deduplication_key = chunk.text.strip()
            if deduplication_key in seen_texts:
                continue
            seen_texts.add(deduplication_key)

            normalized_text = chunk.text.casefold()
            score = sum(keyword in normalized_text for keyword in keywords)
            if score > 0:
                scored_chunks.append(ScoredChunk(chunk=chunk, score=score))

        scored_chunks.sort(key=lambda item: item.score, reverse=True)
        return scored_chunks[:top_k]


def tokenize(text: str) -> list[str]:
    tokens: list[str] = []
    for raw_token in TOKEN_PATTERN.findall(text or ""):
        normalized_token = raw_token.casefold()
        if _is_chinese_token(normalized_token) and len(normalized_token) > 1:
            tokens.extend(
                normalized_token[index : index + 2]
                for index in range(len(normalized_token) - 1)
            )
        else:
            tokens.append(normalized_token)
    return tokens


def _is_chinese_token(token: str) -> bool:
    return all("\u4e00" <= character <= "\u9fff" for character in token)
