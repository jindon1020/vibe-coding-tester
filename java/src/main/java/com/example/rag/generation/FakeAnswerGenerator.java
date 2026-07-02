package com.example.rag.generation;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.stream.Stream;

public class FakeAnswerGenerator implements AnswerGenerator {
    private final List<String> prompts = new ArrayList<>();

    @Override
    public Stream<String> stream(String prompt) {
        prompts.add(prompt);
        return Stream.of("FAKE_RAG_ANSWER:", prompt.substring(0, Math.min(80, prompt.length())));
    }

    public List<String> prompts() {
        return Collections.unmodifiableList(new ArrayList<>(prompts));
    }
}

