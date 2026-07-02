package com.example.rag.domain;

public class ScoredChunk {
    private final DocumentChunk chunk;
    private final int score;

    public ScoredChunk(DocumentChunk chunk, int score) {
        this.chunk = chunk;
        this.score = score;
    }

    public DocumentChunk chunk() {
        return chunk;
    }

    public int score() {
        return score;
    }
}
