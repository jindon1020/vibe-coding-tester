package com.example.rag.retrieval;

import com.example.rag.domain.DocumentChunk;
import com.example.rag.domain.ScoredChunk;

import java.util.List;

public class KeywordRetriever {
    public List<ScoredChunk> retrieve(String query, List<DocumentChunk> chunks, int topK) {
        /*
         * TODO: Candidate should implement this method.
         * Expected behavior:
         * - Tokenize query case-insensitively.
         * - Score each chunk by matched keyword count.
         * - Drop zero-score chunks.
         * - Deduplicate identical chunk text.
         * - Sort by score descending, then stable original order.
         */
        throw new UnsupportedOperationException("TODO");
    }
}
