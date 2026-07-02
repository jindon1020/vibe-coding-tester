# Project Guide

本仓库是一个 RAG 对话服务骨架，用于同时支持 Python 和 Java 两种实现路径。

## Repository Layout

```text
.
├── TASK.md                         # 候选人任务说明
├── docs/
│   └── sample.docx                 # 中文论文测试文档
├── python/                         # Python 实现骨架，包名 rag_app
├── java/                           # Java 实现骨架，基础包 com.example.rag
└── .agents/skills/rag-interview-evaluate/
    ├── SKILL.md                    # 项目内辅助 skill
    └── scripts/collect_report.py   # 项目内辅助脚本
```

## Architecture

两种语言的代码结构保持一致，核心链路是：

```text
docx -> chunks -> keyword retrieval -> ranked context -> prompt -> SSE response
```

主要组件：

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

## Constraints

- 项目不依赖数据库、向量库、Redis、MySQL 或 Docker。
- 项目运行不依赖真实大模型调用。
- Java 代码需保持 Java 8 兼容。
- Python 代码需保持 Python 3.10+ 兼容。
- API key、密码、令牌等敏感信息不得写入仓库。
- 如果候选人使用 AI 辅助完成任务，需要把每次发送给 AI 的原始提示词记录到 `.agents/prompt_record.md`，用于评估 AI 使用过程。
- `.agents/prompt_record.md` 只记录任务相关提示词、采纳情况和简要说明，不得记录真实 API key、密码、令牌或其他敏感信息。

## Prohibited Changes

- 禁止修改测试用例文件：
  - `python/tests/test_rag_contract.py`
  - `java/src/test/java/com/example/rag/RagContractTest.java`
- 禁止删除、跳过、重命名或弱化已有测试。
- 禁止修改 `docs/sample.docx` 来适配实现。
- 禁止修改 `.agents/skills/rag-interview-evaluate/` 下的任何文件。
- 禁止把测试断言、测试关键词、测试期望结果硬编码进业务实现。
- 禁止让 AI 根据测试用例逐条反推最小通过代码；实现必须面向 `TASK.md` 中的业务需求。
- 禁止通过判断文件名、测试类名、测试函数名、固定查询文本等方式返回特殊结果。
- 禁止在业务代码中读取测试文件内容或依赖测试目录路径。
- 禁止用固定字符串列表替代真实 `.docx` 解析。
- 禁止为了通过测试而改变 HTTP 接口语义、SSE 事件格式或模型类的公开字段。
- 禁止引入会掩盖失败的异常吞噬逻辑，例如捕获所有异常后返回空结果。
- 禁止提交本地虚拟环境、构建产物、缓存文件或 IDE 私有配置。

## Expected Implementation Style

- 实现应围绕通用 RAG 检索流程，而不是围绕某一条测试数据。
- 每个组件应保持单一职责，避免把解析、召回、prompt 组装和服务编排写在同一个大函数里。
- 允许使用轻量标准库或项目已有依赖，不要为了简单功能引入重框架。
- 对空输入、无召回、重复内容、文件不存在等情况保持可解释行为。
