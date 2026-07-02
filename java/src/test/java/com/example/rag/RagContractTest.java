package com.example.rag;

import static org.assertj.core.api.Assertions.assertThat;

import com.example.rag.document.DocxLoader;
import com.example.rag.domain.DocumentChunk;
import com.example.rag.domain.ScoredChunk;
import com.example.rag.generation.FakeAnswerGenerator;
import com.example.rag.knowledge.InMemoryKnowledgeBase;
import com.example.rag.prompt.PromptBuilder;
import com.example.rag.retrieval.KeywordRetriever;
import com.example.rag.service.RagService;

import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

import org.apache.poi.xwpf.usermodel.XWPFDocument;
import org.apache.poi.xwpf.usermodel.XWPFParagraph;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

class RagContractTest {
    @TempDir
    Path tempDir;

    @Test
    void docxLoaderExtractsNonEmptyParagraphs() throws IOException {
        Path docx = tempDir.resolve("policy.docx");
        createDocx(docx, Arrays.asList("报销需要发票和审批单", "", "差旅报销需要行程单"));

        List<DocumentChunk> chunks = new DocxLoader().load(docx);

        assertThat(chunks).extracting(DocumentChunk::text)
                .containsExactly("报销需要发票和审批单", "差旅报销需要行程单");
        assertThat(chunks.get(0).source()).endsWith("policy.docx");
        assertThat(chunks.get(0).id()).isNotEqualTo(chunks.get(1).id());
    }

    @Test
    void docxLoaderReadsDownloadedFixture() {
        List<DocumentChunk> chunks = new DocxLoader().load(sampleDocx());
        List<String> texts = chunks.stream().map(DocumentChunk::text).collect(Collectors.toList());

        assertThat(texts)
                .contains("基于 Q-Learning 算法的走迷宫智能体复现与分析");
        assertThat(texts)
                .anyMatch(text -> text.contains("强化学习作为机器学习的重要范式"));
        assertThat(texts)
                .anyMatch(text -> text.contains("马尔可夫决策过程"));
    }

    @Test
    void keywordRetrieverRanksAndDeduplicates() {
        List<DocumentChunk> chunks = Arrays.asList(
                new DocumentChunk("1", "a", "报销 需要 发票 审批单"),
                new DocumentChunk("2", "a", "报销 需要 发票 审批单"),
                new DocumentChunk("3", "b", "请假 需要 审批")
        );

        List<ScoredChunk> results = new KeywordRetriever().retrieve("报销 发票", chunks, 5);

        assertThat(results).hasSize(1);
        assertThat(results.get(0).chunk().id()).isEqualTo("1");
        assertThat(results.get(0).score()).isGreaterThanOrEqualTo(2);
    }

    @Test
    void keywordRetrieverReturnsAccurateTopMatchFromFixture() {
        List<DocumentChunk> chunks = new DocxLoader().load(sampleDocx());

        List<ScoredChunk> experimentResults = new KeywordRetriever().retrieve(
                "成功率 100 平均步数 11.33 最优路径",
                chunks,
                3
        );
        List<ScoredChunk> replayProcessResults = new KeywordRetriever().retrieve(
                "卡片 牌堆 回放 episode 奖励 转移",
                chunks,
                3
        );

        assertThat(experimentResults).isNotEmpty();
        assertThat(experimentResults.get(0).chunk().text()).contains("成功率即达到 100%");
        assertThat(experimentResults.get(0).chunk().text()).contains("11.33 步");
        assertThat(replayProcessResults).isNotEmpty();
        assertThat(replayProcessResults.get(0).chunk().text()).contains("回放该卡片");
        assertThat(replayProcessResults.get(0).chunk().text()).contains("获得奖励");
    }

    @Test
    void promptBuilderIncludesContextAndQuestion() {
        List<ScoredChunk> scored = new KeywordRetriever().retrieve(
                "报销 发票",
                Arrays.asList(new DocumentChunk("1", "policy.docx", "报销需要发票")),
                1
        );

        String prompt = new PromptBuilder().build("报销要什么？", scored);

        assertThat(prompt).contains("报销需要发票");
        assertThat(prompt).contains("报销要什么？");
        assertThat(prompt).contains("policy.docx");
    }

    @Test
    void ragServiceReturnsFallbackWithoutGeneratingAnswer() throws IOException {
        Path docx = tempDir.resolve("policy.docx");
        createDocx(docx, Arrays.asList("报销需要发票"));
        FakeAnswerGenerator fakeGenerator = new FakeAnswerGenerator();
        RagService service = new RagService(
                new InMemoryKnowledgeBase(),
                new KeywordRetriever(),
                new PromptBuilder(),
                fakeGenerator
        );

        List<String> answer = service.chatStream("年假规则是什么？", Arrays.asList(docx.toString()), 3)
                .collect(Collectors.toList());

        assertThat(answer).containsExactly(RagService.NO_CONTEXT_MESSAGE);
        assertThat(fakeGenerator.prompts()).isEmpty();
    }

    @Test
    void ragServiceStreamsGeneratedAnswerWhenContextExists() throws IOException {
        Path docx = tempDir.resolve("policy.docx");
        createDocx(docx, Arrays.asList("报销需要发票和审批单"));
        FakeAnswerGenerator fakeGenerator = new FakeAnswerGenerator();
        RagService service = new RagService(
                new InMemoryKnowledgeBase(),
                new KeywordRetriever(),
                new PromptBuilder(),
                fakeGenerator
        );

        String answer = service.chatStream("报销需要什么？", Arrays.asList(docx.toString()), 3)
                .reduce("", String::concat);

        assertThat(answer).startsWith("FAKE_RAG_ANSWER:");
        assertThat(fakeGenerator.prompts()).hasSize(1);
    }

    private static void createDocx(Path path, List<String> paragraphs) throws IOException {
        try (XWPFDocument document = new XWPFDocument()) {
            for (String text : paragraphs) {
                XWPFParagraph paragraph = document.createParagraph();
                paragraph.createRun().setText(text);
            }
            document.write(java.nio.file.Files.newOutputStream(path));
        }
    }

    private static Path sampleDocx() {
        return Paths.get("..", "docs", "sample.docx").toAbsolutePath().normalize();
    }
}
