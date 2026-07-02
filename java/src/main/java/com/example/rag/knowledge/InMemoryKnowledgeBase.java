package com.example.rag.knowledge;

import com.example.rag.document.DocxLoader;
import com.example.rag.domain.DocumentChunk;

import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class InMemoryKnowledgeBase {
    private final DocxLoader loader;
    private final List<DocumentChunk> chunks = new ArrayList<>();

    public InMemoryKnowledgeBase() {
        this(new DocxLoader());
    }

    public InMemoryKnowledgeBase(DocxLoader loader) {
        this.loader = loader;
    }

    public List<DocumentChunk> chunks() {
        return Collections.unmodifiableList(new ArrayList<>(chunks));
    }

    public List<DocumentChunk> loadDocuments(List<Path> paths) {
        /*
         * TODO: Candidate should implement this method.
         * Expected behavior:
         * - Clear previous chunks before loading.
         * - Load every path with DocxLoader.
         * - Keep chunks in memory.
         */
        throw new UnsupportedOperationException("TODO");
    }
}
