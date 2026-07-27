# Python RAG 实现交付清单

## 1. 基本信息

| 项目 | 内容 |
| --- | --- |
| 开发分支 | `test/zhangchaoyang_0727` |
| 实现语言 | Python 3.10+ |
| 核心实现提交 | `f808e32 feat: implement Python RAG pipeline` |
| 核心链路 | `docx -> chunks -> keyword retrieval -> ranked context -> prompt -> SSE response` |
| 官方测试结果 | `7 passed in 0.67s` |

## 2. 功能完成清单

- [x] 从 `.docx` 读取有效文本
- [x] 忽略空白段落
- [x] 为文本片段生成稳定 ID
- [x] 将多个文档加载到内存知识库
- [x] 根据用户问题执行关键词召回
- [x] 支持英文大小写归一化
- [x] 支持中文自然语言问题的二元词组切分
- [x] 过滤零相关度结果
- [x] 对重复正文去重
- [x] 按相关度稳定排序
- [x] 支持 `top_k` 截断
- [x] 组装带来源、相关度和正文的 RAG Prompt
- [x] 无相关内容时返回兜底结果
- [x] 通过模拟生成器流式返回回答
- [x] SSE 正常发送结束事件 `[DONE]`
- [x] 记录任务相关 AI 原始提示词

## 3. 文件修改清单

### `.agents/prompt_record.md`

- 记录任务分析、编码、方案追问、继续完成等原始提示词。
- 记录每次提示词的采纳情况和简要说明。
- 未记录 API key、密码、令牌等敏感信息。

### `python/src/rag_app/document/docx_loader.py`

- 使用 `python-docx` 的 `Document` 读取 Word 文档。
- 检查目标文件是否为 `.docx`。
- 文件不存在时抛出明确的 `FileNotFoundError`。
- 删除段落首尾空白并忽略空段落。
- 每个有效段落生成一个 `DocumentChunk`。
- chunk ID 格式为 `<filename>#<index>`。

### `python/src/rag_app/knowledge/knowledge_base.py`

- 每次加载文档前清空旧 chunk，避免请求间残留。
- 按输入顺序加载多个文档。
- 将所有 chunk 保存到内存。
- 返回 chunk 列表副本，避免外部直接修改内部状态。

### `python/src/rag_app/retrieval/keyword_retriever.py`

- 英文和数字按完整单词切分，并使用 `casefold()` 进行大小写归一化。
- 连续中文文本切分为二元词组，提高自然语言问题的召回能力。
- 查询词去重，避免相同查询词重复增加分数。
- 以“命中的不同查询关键词数量”作为相关度分数。
- 删除零分结果。
- 相同正文只保留第一次出现的 chunk。
- 按分数降序排序；同分结果利用 Python 稳定排序保持原始顺序。
- 最后截取 `top_k` 条结果。
- 对空查询和非正数 `top_k` 返回空结果。

### `python/src/rag_app/prompt/prompt_builder.py`

- 添加“仅根据上下文回答”的系统指令。
- 上下文中包含序号、文档来源、相关度和正文。
- 在 Prompt 末尾加入用户问题和回答标识。
- 保证生成格式固定、可测试。

### `python/src/rag_app/service/rag_service.py`

- 编排知识库加载、关键词召回、Prompt 构建和回答生成。
- 无召回结果时直接输出 `未找到相关资料`。
- 无上下文时不调用回答生成器。
- 有上下文时转发 `AnswerGenerator.stream()` 的异步输出。

## 4. 数据切分与检索方案

### 数据切分

当前按 Word 非空段落切分，一个有效段落对应一个 chunk。不使用固定字符长度、滑动窗口或语义切分。

选择该方案的原因：

- 与题目要求一致。
- 保留论文段落的自然语义边界。
- 实现简单且结果稳定。
- 不需要引入额外分词或文档处理依赖。

### 检索与排序

当前采用轻量关键词检索：

1. 英文按单词切分，中文按二元词组切分。
2. 计算每个 chunk 命中的不同查询词数量。
3. 删除零分和重复正文。
4. 按分数降序排列。
5. 同分时保持文档原始顺序。
6. 返回前 `top_k` 条。

当前没有实现：

- BM25
- embedding 向量检索
- 向量数据库
- cross-encoder 或 LLM 重排序器

这些能力不属于本题要求，并且题目明确要求不引入向量库或外部服务。

## 5. 测试方法

Windows PowerShell：

```powershell
cd python
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m pytest -q
```

如果已有 `%TEMP%\pytest-of-<用户名>` 目录存在 ACL 权限冲突，可改用当前用户创建的唯一临时目录，并关闭可选 pytest 缓存：

```powershell
$pytestTemp = Join-Path $env:TEMP ("rag-pytest-" + [guid]::NewGuid().ToString("N"))
.\.venv\Scripts\python.exe -m pytest -q --basetemp="$pytestTemp" -p no:cacheprovider
```

Linux/macOS：

```bash
cd python
python3 -m venv .venv
./.venv/bin/pip install -e ".[dev]"
./.venv/bin/pytest -q
```

## 6. 实际测试结果

### 官方 pytest

```text
.......                                                                  [100%]
7 passed in 0.67s
```

### 补充验证

- [x] 所有 Python 源码通过语法解析检查
- [x] 18 项 loader、retrieval、prompt、service 冒烟断言通过
- [x] 真实 `docs/sample.docx` 成功解析为 149 个非空 chunk
- [x] 所有 chunk ID 唯一
- [x] SSE 最终输出 `event: done` 和 `[DONE]`
- [x] `git diff --check` 通过

## 7. 未修改内容

- 未修改 `python/tests/test_rag_contract.py`
- 未修改 Java 测试或实现
- 未修改 `docs/sample.docx`
- 未修改 `.agents/skills/rag-interview-evaluate/`
- 未引入数据库、Redis、向量库、Docker 或真实大模型调用
- 未写入 API key、密码或令牌

## 8. Git 状态说明

核心实现已保存在本地提交：

```text
f808e32 feat: implement Python RAG pipeline
```

远程推送失败，原因是当前 GitHub 用户 `johnzhang777` 对仓库 `jindon1020/vibe-coding-tester` 没有写权限：

```text
remote: Permission to jindon1020/vibe-coding-tester.git denied to johnzhang777.
fatal: unable to access repository: HTTP 403
```

获得写权限或配置可写 fork 后，可执行：

```powershell
git push origin test/zhangchaoyang_0727
```

本交付报告是在核心实现提交之后创建的，尚未包含在 `f808e32` 中。
