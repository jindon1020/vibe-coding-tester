# Claude Code Guide

本仓库是一个 RAG 对话服务骨架，用于同时支持 Python 和 Java 两种实现路径。Claude Code 在本仓库中工作时，应优先完成 `TASK.md` 中定义的候选人任务，并严格遵守本文件的边界。

## 工作方式

1. 先阅读 `TASK.md` 和本文件，再开始修改代码。
2. 只选择 `python/` 或 `java/` 其中一种语言路径完成实现，不要同时重写两套实现。
3. 修改应围绕通用 RAG 流程：`docx -> chunks -> keyword retrieval -> ranked context -> prompt -> SSE response`。
4. 使用 AI 辅助时，把每次发送给 AI 的原始提示词记录到 `.agents/prompt_record.md`，并写明采纳情况和简要说明。
5. 不要在 `.agents/prompt_record.md` 或任何仓库文件中记录真实 API key、密码、令牌或其他敏感信息。
6. 完成后运行所选语言的测试，并在交付说明中写清楚选择的语言和测试结果。

## 仓库结构

```text
.
├── TASK.md                         # 候选人任务说明
├── docs/
│   └── sample.docx                 # 中文论文测试文档
├── python/                         # Python 实现骨架，包名 rag_app
├── java/                           # Java 实现骨架，基础包 com.example.rag
└── .agents/skills/rag-interview-evaluate/
    ├── SKILL.md                    # 项目内评估 skill
    └── scripts/collect_report.py   # 项目内评估脚本
```

## 架构约定

两种语言的代码结构保持一致：

| 层 | Python 包 | Java 包 | 职责 |
| --- | --- | --- | --- |
| domain | `rag_app.domain` | `com.example.rag.domain` | 请求对象、文档片段、召回结果等数据模型 |
| document | `rag_app.document` | `com.example.rag.document` | 读取 `.docx` 中的非空段落 |
| knowledge | `rag_app.knowledge` | `com.example.rag.knowledge` | 维护内存中的文档 chunk |
| retrieval | `rag_app.retrieval` | `com.example.rag.retrieval` | 根据查询关键词召回并排序 chunk |
| prompt | `rag_app.prompt` | `com.example.rag.prompt` | 把问题和召回上下文组装为 prompt |
| generation | `rag_app.generation` | `com.example.rag.generation` | 本地模拟回答生成，不调用真实大模型 |
| service | `rag_app.service` | `com.example.rag.service` | 编排加载、召回、prompt 生成和回答生成 |
| api/web | `rag_app.api` | `com.example.rag.web` | 提供 `POST /api/chat/stream` SSE 接口 |
| config | - | `com.example.rag.config` | Java Spring Bean 装配 |

## 实现要求

- 从 `.docx` 中读取有效文本，忽略空段落。
- 把文档内容放入内存知识库；重新加载时清空旧内容。
- 根据问题做确定性的关键词召回。
- 召回结果按分数降序排序；同分时保持稳定顺序。
- 对重复内容进行处理，避免重复 chunk 干扰结果。
- 基于召回内容生成包含上下文、来源信息、分数和问题的 prompt。
- 无相关内容时返回 `未找到相关资料`，并且不要调用回答生成器。
- 流式接口必须正常结束，保留最终 `done` 事件。
- Python 代码保持 Python 3.10+ 兼容；Java 代码保持 Java 8 兼容。

## 禁止事项

- 禁止修改测试用例文件：
  - `python/tests/test_rag_contract.py`
  - `java/src/test/java/com/example/rag/RagContractTest.java`
- 禁止删除、跳过、重命名或弱化已有测试。
- 禁止修改 `docs/sample.docx` 来适配实现。
- 禁止修改 `.agents/skills/rag-interview-evaluate/` 下的任何文件。
- 禁止把测试断言、测试关键词、测试期望结果硬编码进业务实现。
- 禁止根据测试用例逐条反推最小通过代码；实现必须面向 `TASK.md` 中的业务需求。
- 禁止通过判断文件名、测试类名、测试函数名、固定查询文本等方式返回特殊结果。
- 禁止在业务代码中读取测试文件内容或依赖测试目录路径。
- 禁止用固定字符串列表替代真实 `.docx` 解析。
- 禁止为了通过测试而改变 HTTP 接口语义、SSE 事件格式或模型类的公开字段。
- 禁止引入数据库、向量库、Redis、MySQL、Docker、真实大模型调用或外部服务。
- 禁止引入会掩盖失败的异常吞噬逻辑，例如捕获所有异常后返回空结果。
- 禁止提交本地虚拟环境、构建产物、缓存文件或 IDE 私有配置。

## 自测命令

Python：

```bash
cd python
python3 -m venv .venv
./.venv/bin/pip install -e ".[dev]"
./.venv/bin/pytest
```

Java：

```bash
cd java
mvn test
```

## 交付说明

最终回复应包含：

- 选择的语言路径。
- 完成的核心能力。
- 执行过的测试命令和结果。
- 若测试未能执行，说明具体原因。
