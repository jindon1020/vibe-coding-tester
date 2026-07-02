from __future__ import annotations

from collections.abc import AsyncIterator

from rag_app.generation.answer_generator import AnswerGenerator
from rag_app.knowledge.knowledge_base import InMemoryKnowledgeBase
from rag_app.prompt.prompt_builder import PromptBuilder
from rag_app.retrieval.keyword_retriever import KeywordRetriever


NO_CONTEXT_MESSAGE = "未找到相关资料"


class RagService:
    def __init__(
        self,
        knowledge_base: InMemoryKnowledgeBase,
        retriever: KeywordRetriever,
        prompt_builder: PromptBuilder,
        answer_generator: AnswerGenerator,
    ) -> None:
        self.knowledge_base = knowledge_base
        self.retriever = retriever
        self.prompt_builder = prompt_builder
        self.answer_generator = answer_generator

    async def chat_stream(
        self,
        question: str,
        doc_paths: list[str],
        top_k: int = 3,
    ) -> AsyncIterator[str]:
        """Run the full RAG flow and yield answer chunks.

        Expected behavior:
        - Load documents into the in-memory knowledge base.
        - Retrieve top_k chunks.
        - If no chunks are retrieved, yield NO_CONTEXT_MESSAGE and do not generate an answer.
        - Build prompt and stream output from the local answer generator.
        """
        chunks = self.knowledge_base.load_documents(doc_paths)
        retrieved_chunks = self.retriever.retrieve(question, chunks, top_k)

        if not retrieved_chunks:
            yield NO_CONTEXT_MESSAGE
            return

        prompt = self.prompt_builder.build(question, retrieved_chunks)
        async for chunk in self.answer_generator.stream(prompt):
            yield chunk
