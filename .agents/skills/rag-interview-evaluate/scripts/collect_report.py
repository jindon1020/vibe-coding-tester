from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]


def run(command: list[str], cwd: Path = ROOT) -> tuple[int, str]:
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=120,
            check=False,
        )
    except FileNotFoundError as exc:
        return 127, str(exc)
    except subprocess.TimeoutExpired as exc:
        return 124, (exc.stdout or "") + "\nTIMEOUT"
    return completed.returncode, completed.stdout


def score_tests(language: str) -> tuple[int, str, int]:
    if language == "python":
        code, output = run(["python3", "-m", "pytest", "-q"], ROOT / "python")
    else:
        with tempfile.TemporaryDirectory(prefix="rag-interview-m2-") as maven_repo:
            code, output = run(
                ["mvn", f"-Dmaven.repo.local={maven_repo}", "test", "-q"],
                ROOT / "java",
            )
    return (30 if code == 0 else 0), output, code


def score_static(language: str) -> tuple[int, list[str]]:
    base = ROOT / language
    findings: list[str] = []
    score = 15

    files = list((base / "src").rglob("*.py" if language == "python" else "*.java"))
    text_by_file = {file: file.read_text(encoding="utf-8") for file in files}

    combined = "\n".join(text_by_file.values())
    if "TODO" in combined or "NotImplemented" in combined or "UnsupportedOperationException" in combined:
        score -= 6
        findings.append("仍存在 TODO / 未实现代码")
    if "pt-" in combined or "sk-" in combined:
        score -= 6
        findings.append("疑似硬编码密钥")
    if max((len(content.splitlines()) for content in text_by_file.values()), default=0) > 220:
        score -= 3
        findings.append("存在过长文件，可能职责过重")
    if language == "python" and "async def chat_stream" not in combined:
        score -= 3
        findings.append("RagService 未保留异步流式接口")
    if language == "java" and "Stream<String> chatStream" not in combined:
        score -= 3
        findings.append("RagService 未保留 Stream 接口")

    return max(score, 0), findings


def load_score(language: str) -> dict:
    test_score, test_output, test_exit_code = score_tests(language)
    static_score, findings = score_static(language)
    return {
        "language": language,
        "score": test_score + static_score,
        "max_score_by_script": 45,
        "unit_test_score": test_score,
        "static_score": static_score,
        "manual_score_remaining": 55,
        "manual_score_components": {
            "implementation_review": 35,
            "ai_process": 20,
        },
        "findings": findings,
        "test_output_tail": "\n".join(test_output.splitlines()[-40:]),
        "test_command_exit_code": test_exit_code,
    }


def git_output(args: list[str]) -> str:
    code, output = run(["git"] + args)
    if code != 0:
        return output.strip()
    return output.strip()


def prompt_log_summary() -> dict:
    path = ROOT / ".ai-interview" / "prompts.md"
    if not path.exists():
        return {"exists": False, "meaningful_entries": 0, "preview": ""}
    text = path.read_text(encoding="utf-8")
    meaningful_entries = 0
    current_has_content = False
    ignored_exact = {
        "- 时间：",
        "- 当前目标：",
        "- 原始指令：",
        "- 期望产出：",
        "- 是否采纳：",
        "- 未采纳原因：",
        "```text",
        "```",
        "在这里粘贴发给 AI 的原始指令。",
    }
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## Prompt "):
            if current_has_content:
                meaningful_entries += 1
            current_has_content = False
            continue
        if (
            not stripped
            or stripped.startswith("#")
            or stripped in ignored_exact
            or stripped.startswith("候选人使用 ")
            or stripped.startswith("不要记录真实 ")
        ):
            continue
        current_has_content = True
    if current_has_content:
        meaningful_entries += 1
    return {
        "exists": True,
        "meaningful_entries": meaningful_entries,
        "preview": "\n".join(text.splitlines()[:80]),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--language", choices=["python", "java"], required=True)
    args = parser.parse_args()

    score = load_score(args.language)
    diff_stat = git_output(["diff", "--stat", "master...HEAD"])
    if "fatal:" in diff_stat.lower() or not diff_stat:
        diff_stat = git_output(["diff", "--stat", "--", "."])
    status = git_output(["status", "--short"])

    result = {
        "language": args.language,
        "automatic_score": score,
        "prompt_log": prompt_log_summary(),
        "git_status_short": status,
        "git_diff_stat": diff_stat,
        "next_steps_for_agent": [
            "Inspect implementation files for the selected language.",
            "Inspect .ai-interview/prompts.md if present for AI process evidence.",
            "Assign RAG code review score out of 35.",
            "Assign AI process score out of 20.",
            "Return the final evaluation in the SKILL.md output format.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
