from __future__ import annotations

from collections.abc import AsyncIterator


class AnswerGenerator:
    async def stream(self, prompt: str) -> AsyncIterator[str]:
        raise NotImplementedError


class FakeAnswerGenerator(AnswerGenerator):
    def __init__(self) -> None:
        self.prompts: list[str] = []

    async def stream(self, prompt: str) -> AsyncIterator[str]:
        self.prompts.append(prompt)
        yield "FAKE_RAG_ANSWER:"
        yield prompt[:80]

