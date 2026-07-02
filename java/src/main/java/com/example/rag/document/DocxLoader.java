package com.example.rag.document;

import com.example.rag.domain.DocumentChunk;

import java.nio.file.Path;
import java.util.List;

public class DocxLoader {
    public List<DocumentChunk> load(Path path) {
        /*
         * TODO: Candidate should implement this method.
         * Expected behavior:
         * - Read a .docx file.
         * - Ignore empty paragraphs.
         * - Return one DocumentChunk per paragraph.
         * - Use stable chunk ids such as "<filename>#<index>".
         */
        throw new UnsupportedOperationException("TODO");
    }
}
