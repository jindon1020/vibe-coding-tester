from __future__ import annotations

from rag_app.domain.models import ScoredChunk


class PromptBuilder:
    def build(self, question: str, chunks: list[ScoredChunk]) -> str:
        """Build a RAG prompt from question and retrieved chunks.

        TODO: Candidate should implement this method.
        Expected behavior:
        - Include a short instruction that answers must be based on context.
        - Include each context chunk with source and score.
        - Include the user's question.
        """
        raise NotImplementedError

