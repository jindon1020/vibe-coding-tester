from __future__ import annotations

from rag_app.domain.models import ScoredChunk


class PromptBuilder:
    def build(self, question: str, chunks: list[ScoredChunk]) -> str:
        """Build a RAG prompt from question and retrieved chunks.

        Expected behavior:
        - Include a short instruction that answers must be based on context.
        - Include each context chunk with source and score.
        - Include the user's question.
        """
        context_lines = [
            f"[{index}] source={scored.chunk.source} score={scored.score} text={scored.chunk.text}"
            for index, scored in enumerate(chunks, start=1)
        ]
        context_block = "\n".join(context_lines)

        return (
            "请仅基于下面提供的上下文回答问题。如果上下文不足，请明确说明。\n"
            f"上下文:\n{context_block}\n"
            f"问题:\n{question}"
        )
