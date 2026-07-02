package com.example.rag.service;

import com.example.rag.generation.AnswerGenerator;
import com.example.rag.knowledge.InMemoryKnowledgeBase;
import com.example.rag.prompt.PromptBuilder;
import com.example.rag.retrieval.KeywordRetriever;

import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class RagService {
    public static final String NO_CONTEXT_MESSAGE = "未找到相关资料";

    private final InMemoryKnowledgeBase knowledgeBase;
    private final KeywordRetriever retriever;
    private final PromptBuilder promptBuilder;
    private final AnswerGenerator answerGenerator;

    public RagService(
            InMemoryKnowledgeBase knowledgeBase,
            KeywordRetriever retriever,
            PromptBuilder promptBuilder,
            AnswerGenerator answerGenerator
    ) {
        this.knowledgeBase = knowledgeBase;
        this.retriever = retriever;
        this.promptBuilder = promptBuilder;
        this.answerGenerator = answerGenerator;
    }

    public Stream<String> chatStream(String question, List<String> docPaths, int topK) {
        /*
         * TODO: Candidate should implement this method.
         * Expected behavior:
         * - Load documents into the in-memory knowledge base.
         * - Retrieve top_k chunks.
         * - If no chunks are retrieved, return Stream.of(NO_CONTEXT_MESSAGE) and do not generate an answer.
         * - Build prompt and stream output from the local answer generator.
         */
        throw new UnsupportedOperationException("TODO");
    }

    protected List<Path> toPaths(List<String> docPaths) {
        return docPaths.stream().map(Paths::get).collect(Collectors.toList());
    }
}
