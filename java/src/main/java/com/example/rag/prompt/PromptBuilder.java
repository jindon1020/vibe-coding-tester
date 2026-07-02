package com.example.rag.prompt;

import com.example.rag.domain.ScoredChunk;

import java.util.List;

public class PromptBuilder {
    public String build(String question, List<ScoredChunk> chunks) {
        /*
         * TODO: Candidate should implement this method.
         * Expected behavior:
         * - Include a short instruction that answers must be based on context.
         * - Include each context chunk with source and score.
         * - Include the user's question.
         */
        throw new UnsupportedOperationException("TODO");
    }
}
