from __future__ import annotations

from collections.abc import AsyncIterator

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from rag_app.generation.answer_generator import FakeAnswerGenerator
from rag_app.knowledge.knowledge_base import InMemoryKnowledgeBase
from rag_app.domain.models import ChatRequest
from rag_app.prompt.prompt_builder import PromptBuilder
from rag_app.service.rag_service import RagService
from rag_app.retrieval.keyword_retriever import KeywordRetriever


router = APIRouter()


def get_rag_service() -> RagService:
    return RagService(
        knowledge_base=InMemoryKnowledgeBase(),
        retriever=KeywordRetriever(),
        prompt_builder=PromptBuilder(),
        answer_generator=FakeAnswerGenerator(),
    )


@router.post("/api/chat/stream")
async def chat_stream(
    request: ChatRequest,
    service: RagService = Depends(get_rag_service),
) -> StreamingResponse:
    return StreamingResponse(
        _to_sse(service.chat_stream(request.question, request.doc_paths, request.top_k)),
        media_type="text/event-stream",
    )


async def _to_sse(chunks: AsyncIterator[str]) -> AsyncIterator[str]:
    async for chunk in chunks:
        yield f"event: message\ndata: {chunk}\n\n"
    yield "event: done\ndata: [DONE]\n\n"
