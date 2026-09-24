import os
import requests


def post_pr_comment(report_content):
    """Post the review report as a comment on the current PR."""
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")  # e.g. "username/repo-name"
    pr_number = os.environ.get("PR_NUMBER")

    if not all([token, repo, pr_number]):
        print("Missing GitHub Actions environment variables. Skipping comment post.")
        return

    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    body = report_content[:65000]

    response = requests.post(url, headers=headers, json={"body": body})

    if response.status_code == 201:
        print("Comment posted successfully!")
    else:
        print(f"Failed to post comment: {response.status_code} - {response.text}")


if __name__ == "__main__":
    with open("review_report.md", "r", encoding="utf-8") as f:
        content = f.read()
    post_pr_comment(content)