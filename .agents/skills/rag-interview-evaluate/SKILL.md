---
name: rag-interview-evaluate
description: Run the full RAG interview evaluation for a candidate branch, including automatic tests, static checks, code review score, AI prompt process score, and final 100-point result. Use when asked to score, evaluate, grade, or验收 a candidate solution in this repository.
---

# RAG Interview Evaluation

Use this skill to produce one complete candidate assessment.

## Inputs

Ask for the language only if it is not obvious from the candidate's implementation:

- `python`
- `java`

Default to the language with meaningful candidate changes if only one side was edited.

## Required Workflow

1. Run the bundled report script:

   ```bash
   python3 .agents/skills/rag-interview-evaluate/scripts/collect_report.py --language <python|java>
   ```

2. Inspect the changed implementation files for the selected language.

3. Inspect `.ai-interview/prompts.md` if it exists.

4. If available, inspect `git diff master...HEAD`. If the repository has no master reference or this fails, use `git diff -- .`.

5. Produce a final score out of 100:

   - Automatic score from script: 45 points
   - RAG code review: 35 points
   - AI process review: 20 points

Do not mechanically give full manual points. Ground every manual score in evidence from code, tests, prompt log, and diff.

## RAG Code Review, 35 Points

Score implementation quality:

- New feature completeness, 20:
  - Loads non-empty `.docx` paragraphs.
  - Stores chunks in memory and clears old chunks on reload.
  - Implements deterministic keyword retrieval.
  - Sorts by score descending and preserves stable order for ties.
  - Deduplicates identical chunk text.
  - Builds prompt with instruction, context, source metadata, score, and question.
  - Generates answer only after context exists.

- Change handling, 10:
  - No-context path returns `未找到相关资料`.
  - No-context path does not call `AnswerGenerator`.
  - SSE contract keeps final `done` event.
  - Implementation stays compatible with Java 8 or Python 3.10+.

- Code quality and safety, 5:
  - Clear layering across loader, knowledge base, retriever, prompt builder, service.
  - No hardcoded answers for fixture-specific keywords.
  - No hardcoded secrets.
  - Small, readable methods with limited branching.

## AI Process Review, 20 Points

Score process quality from `.ai-interview/prompts.md` if present, plus observed evidence:

- Demand clarification, 3
- Context gathering, 3
- Task decomposition, 3
- Scope control, 3
- Testing and debugging, 3
- Code review awareness, 2
- Change handling, 2
- Log integrity, 1

If the prompt log is missing or empty, rely more heavily on interviewer notes, git diff, and visible workflow evidence. Do not automatically fail the candidate solely because the prompt log is absent.

## Output Format

Return this exact structure:

```text
RAG Interview Evaluation

Language: <python|java>
Final Score: <n>/100

Score Breakdown:
- Automatic tests/static: <n>/45
- RAG code review: <n>/35
- AI process review: <n>/20

Automatic Result:
- Unit tests: <n>/30
- Static checks: <n>/15
- Key output: <brief summary>

Findings:
- [P0/P1/P2] ...

AI Process Evidence:
- ...

Risks / Possible Test Gaming:
- ...

Recommended Decision:
- Strong pass / Pass / Borderline / No pass
```

## Decision Guidance

- Strong pass: 85+ with credible AI process evidence and clean code.
- Pass: 70-84 with tests passing and acceptable code.
- Borderline: 55-69 or strong code with weak process evidence.
- No pass: below 55, failing core tests, hardcoded behavior, or poor process evidence plus poor code.
