package com.example.rag.generation;

import java.util.stream.Stream;

public interface AnswerGenerator {
    Stream<String> stream(String prompt);
}

