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
        sections = [
            "请仅根据以下上下文回答问题。如果上下文不足，请明确说明无法从资料中确定答案。"
        ]
        for index, scored_chunk in enumerate(chunks, start=1):
            sections.append(
                "\n".join(
                    [
                        f"[上下文 {index}]",
                        f"来源: {scored_chunk.chunk.source}",
                        f"相关度: {scored_chunk.score}",
                        f"内容: {scored_chunk.chunk.text}",
                    ]
                )
            )
        sections.append(f"问题: {question.strip()}\n回答:")
        return "\n\n".join(sections)
