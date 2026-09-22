import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def build_prompt(file_results):
    """
    Turn structured findings into a compact prompt for the LLM.
    file_results: list of combined_result dicts from run_pipeline.py
    """
    summary_lines = []
    for r in file_results:
        if not r["ruff_issues"] and not r["bandit_issues"]:
            continue  # skip clean files to keep prompt short

        summary_lines.append(f"File: {r['file']}")
        summary_lines.append(f"  Functions: {[f['name'] for f in r['functions']]}")
        for issue in r["ruff_issues"]:
            summary_lines.append(f"  Ruff (line {issue['line']}): {issue['message']}")
        for issue in r["bandit_issues"]:
            summary_lines.append(f"  Bandit (line {issue['line']}, {issue['severity']}): {issue['message']}")

    findings_text = "\n".join(summary_lines)

    prompt = f"""You are a senior software engineer reviewing a codebase.
Below are structured findings from automated analysis tools (linter and security scanner).

{findings_text}

Write a concise, PR-style code review. For each file with issues:
1. Summarize the key problems in plain English
2. Rate severity (Low/Medium/High)
3. Suggest a specific fix

Keep it professional and actionable, like a real GitHub PR review comment."""

    return prompt


def get_llm_review(file_results):
    """Send findings to Groq and return the generated review text."""
    prompt = build_prompt(file_results)

    if not prompt.strip() or "File:" not in prompt:
        return "No issues found — code looks clean!"

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    # quick standalone test with fake data
    fake_results = [
        {
            "file": "example.py",
            "functions": [{"name": "process_data", "line": 1, "num_args": 2}],
            "classes": [],
            "ruff_issues": [{"line": 5, "code": "E501", "message": "Line too long"}],
            "bandit_issues": [{"line": 10, "severity": "HIGH", "message": "Use of eval() detected"}]
        }
    ]

    review = get_llm_review(fake_results)
    print(review)