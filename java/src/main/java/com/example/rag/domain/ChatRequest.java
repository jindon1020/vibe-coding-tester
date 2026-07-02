package com.example.rag.domain;

import java.util.Collections;
import java.util.List;

public class ChatRequest {
    private String question;
    private List<String> docPaths = Collections.emptyList();
    private int topK = 3;

    public ChatRequest() {
    }

    public ChatRequest(String question, List<String> docPaths, int topK) {
        this.question = question;
        this.docPaths = docPaths;
        this.topK = topK;
    }

    public String question() {
        return question;
    }

    public List<String> docPaths() {
        return docPaths;
    }

    public int topK() {
        return topK;
    }

    public String getQuestion() {
        return question;
    }

    public void setQuestion(String question) {
        this.question = question;
    }

    public List<String> getDocPaths() {
        return docPaths;
    }

    public void setDocPaths(List<String> docPaths) {
        this.docPaths = docPaths;
    }

    public int getTopK() {
        return topK;
    }

    public void setTopK(int topK) {
        this.topK = topK;
    }
}
