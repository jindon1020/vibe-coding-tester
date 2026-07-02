package com.example.rag.config;

import com.example.rag.generation.FakeAnswerGenerator;
import com.example.rag.knowledge.InMemoryKnowledgeBase;
import com.example.rag.prompt.PromptBuilder;
import com.example.rag.retrieval.KeywordRetriever;
import com.example.rag.service.RagService;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class RagServiceFactory {
    @Bean
    public RagService ragService() {
        return new RagService(
                new InMemoryKnowledgeBase(),
                new KeywordRetriever(),
                new PromptBuilder(),
                new FakeAnswerGenerator()
        );
    }
}
