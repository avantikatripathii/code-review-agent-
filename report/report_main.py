from datetime import datetime


def generate_markdown_report(repo_path, all_results, graph, llm_review):
    lines = []

    lines.append(f"# Code Review Report")
    lines.append(f"**Repository:** `{repo_path}`")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("")
    lines.append("---")
    lines.append("")

    lines.append("## Summary")
    total_files = len(all_results)
    total_ruff = sum(len(r["ruff_issues"]) for r in all_results)
    total_bandit = sum(len(r["bandit_issues"]) for r in all_results)
    lines.append(f"- **Files analyzed:** {total_files}")
    lines.append(f"- **Ruff issues found:** {total_ruff}")
    lines.append(f"- **Bandit (security) issues found:** {total_bandit}")
    lines.append(f"- **Dependency graph:** {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges")
    lines.append("")
    lines.append("---")
    lines.append("")

    lines.append("## AI-Generated Review")
    lines.append("")
    lines.append(llm_review)
    lines.append("")
    lines.append("---")
    lines.append("")

    lines.append("## Dependency Graph")
    lines.append("")
    for source, target in graph.edges():
        lines.append(f"- `{source}` → `{target}`")
    lines.append("")

    return "\n".join(lines)


def save_report(content, output_path="review_report.md"):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"\nReport saved to: {output_path}")