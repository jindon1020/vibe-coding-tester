from __future__ import annotations

from dataclasses import dataclass
from pydantic import BaseModel, Field


@dataclass(frozen=True)
class DocumentChunk:
    id: str
    source: str
    text: str


@dataclass(frozen=True)
class ScoredChunk:
    chunk: DocumentChunk
    score: int


class ChatRequest(BaseModel):
    question: str = Field(min_length=1)
    doc_paths: list[str] = Field(default_factory=list)
    top_k: int = Field(default=3, ge=1, le=10)

