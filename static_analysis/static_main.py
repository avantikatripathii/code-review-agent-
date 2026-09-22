import subprocess
import json


def run_ruff(file_path):
    """Run ruff (fast linter) on a file and return list of issues."""
    result = subprocess.run(
        ["ruff", "check", file_path, "--output-format=json"],
        capture_output=True,
        text=True
    )

    if not result.stdout.strip():
        return []

    try:
        issues = json.loads(result.stdout)
    except json.JSONDecodeError:
        return []

    return [
        {
            "line": issue["location"]["row"],
            "code": issue["code"],
            "message": issue["message"]
        }
        for issue in issues
    ]


def run_bandit(file_path):
    """Run bandit (security scanner) on a file and return list of issues."""
    result = subprocess.run(
        ["bandit", "-f", "json", file_path],
        capture_output=True,
        text=True
    )

    if not result.stdout.strip():
        return []

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return []

    return [
        {
            "line": r["line_number"],
            "severity": r["issue_severity"],
            "message": r["issue_text"]
        }
        for r in data.get("results", [])
    ]


def analyze_file_static(file_path):
    """Run all static analysis tools on a file."""
    return {
        "file": file_path,
        "ruff_issues": run_ruff(file_path),
        "bandit_issues": run_bandit(file_path)
    }


if __name__ == "__main__":
    result = analyze_file_static(__file__)
    print(f"File: {result['file']}")
    print(f"Ruff issues: {len(result['ruff_issues'])}")
    for issue in result['ruff_issues']:
        print(f"  Line {issue['line']}: [{issue['code']}] {issue['message']}")
    print(f"Bandit issues: {len(result['bandit_issues'])}")
    for issue in result['bandit_issues']:
        print(f"  Line {issue['line']}: [{issue['severity']}] {issue['message']}")