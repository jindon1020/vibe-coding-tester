package com.example.rag.domain;

public class DocumentChunk {
    private final String id;
    private final String source;
    private final String text;

    public DocumentChunk(String id, String source, String text) {
        this.id = id;
        this.source = source;
        this.text = text;
    }

    public String id() {
        return id;
    }

    public String source() {
        return source;
    }

    public String text() {
        return text;
    }
}
