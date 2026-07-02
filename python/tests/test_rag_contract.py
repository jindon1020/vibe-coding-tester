from __future__ import annotations

from pathlib import Path

import pytest
from docx import Document

from rag_app.generation.answer_generator import FakeAnswerGenerator
from rag_app.document.docx_loader import DocxLoader
from rag_app.knowledge.knowledge_base import InMemoryKnowledgeBase
from rag_app.domain.models import DocumentChunk
from rag_app.prompt.prompt_builder import PromptBuilder
from rag_app.service.rag_service import NO_CONTEXT_MESSAGE, RagService
from rag_app.retrieval.keyword_retriever import KeywordRetriever


FIXTURE_DOCX = Path(__file__).resolve().parents[2] / "docs" / "sample.docx"


def create_docx(path: Path, paragraphs: list[str]) -> None:
    doc = Document()
    for paragraph in paragraphs:
        doc.add_paragraph(paragraph)
    doc.save(path)


def test_docx_loader_extracts_non_empty_paragraphs(tmp_path: Path) -> None:
    docx_path = tmp_path / "policy.docx"
    create_docx(docx_path, ["报销需要发票和审批单", "", "差旅报销需要行程单"])

    chunks = DocxLoader().load(docx_path)

    assert [chunk.text for chunk in chunks] == ["报销需要发票和审批单", "差旅报销需要行程单"]
    assert chunks[0].source.endswith("policy.docx")
    assert chunks[0].id != chunks[1].id


def test_docx_loader_reads_downloaded_fixture() -> None:
    chunks = DocxLoader().load(FIXTURE_DOCX)

    texts = [chunk.text for chunk in chunks]
    assert "基于 Q-Learning 算法的走迷宫智能体复现与分析" in texts
    assert any("强化学习作为机器学习的重要范式" in text for text in texts)
    assert any("马尔可夫决策过程" in text for text in texts)


def test_keyword_retriever_ranks_and_deduplicates() -> None:
    chunks = [
        DocumentChunk(id="1", source="a", text="报销 需要 发票 审批单"),
        DocumentChunk(id="2", source="a", text="报销 需要 发票 审批单"),
        DocumentChunk(id="3", source="b", text="请假 需要 审批"),
    ]

    results = KeywordRetriever().retrieve("报销 发票", chunks, top_k=5)

    assert len(results) == 1
    assert results[0].chunk.id == "1"
    assert results[0].score >= 2


def test_keyword_retriever_returns_accurate_top_match_from_fixture() -> None:
    chunks = DocxLoader().load(FIXTURE_DOCX)

    experiment_results = KeywordRetriever().retrieve(
        "成功率 100 平均步数 11.33 最优路径",
        chunks,
        top_k=3,
    )
    replay_process_results = KeywordRetriever().retrieve(
        "卡片 牌堆 回放 episode 奖励 转移",
        chunks,
        top_k=3,
    )

    assert experiment_results
    assert "成功率即达到 100%" in experiment_results[0].chunk.text
    assert "11.33 步" in experiment_results[0].chunk.text
    assert replay_process_results
    assert "回放该卡片" in replay_process_results[0].chunk.text
    assert "获得奖励" in replay_process_results[0].chunk.text


def test_prompt_builder_includes_context_and_question() -> None:
    scored = KeywordRetriever().retrieve(
        "报销 发票",
        [DocumentChunk(id="1", source="policy.docx", text="报销需要发票")],
        top_k=1,
    )

    prompt = PromptBuilder().build("报销要什么？", scored)

    assert "报销需要发票" in prompt
    assert "报销要什么？" in prompt
    assert "policy.docx" in prompt


@pytest.mark.asyncio
async def test_rag_service_returns_fallback_without_generating_answer(tmp_path: Path) -> None:
    docx_path = tmp_path / "policy.docx"
    create_docx(docx_path, ["报销需要发票"])
    fake_generator = FakeAnswerGenerator()
    service = RagService(
        knowledge_base=InMemoryKnowledgeBase(),
        retriever=KeywordRetriever(),
        prompt_builder=PromptBuilder(),
        answer_generator=fake_generator,
    )

    answer = [chunk async for chunk in service.chat_stream("年假规则是什么？", [str(docx_path)], 3)]

    assert answer == [NO_CONTEXT_MESSAGE]
    assert fake_generator.prompts == []


@pytest.mark.asyncio
async def test_rag_service_streams_generated_answer_when_context_exists(tmp_path: Path) -> None:
    docx_path = tmp_path / "policy.docx"
    create_docx(docx_path, ["报销需要发票和审批单"])
    fake_generator = FakeAnswerGenerator()
    service = RagService(
        knowledge_base=InMemoryKnowledgeBase(),
        retriever=KeywordRetriever(),
        prompt_builder=PromptBuilder(),
        answer_generator=fake_generator,
    )

    answer = [chunk async for chunk in service.chat_stream("报销需要什么？", [str(docx_path)], 3)]

    assert "".join(answer).startswith("FAKE_RAG_ANSWER:")
    assert len(fake_generator.prompts) == 1
