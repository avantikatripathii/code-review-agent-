from parser.parser_main import find_python_files, read_file_content
from ast_analysis.ast_main import analyze_file
from static_analysis.static_main import analyze_file_static
from dependency_graph.graph_main import build_dependency_graph
from llm_reasoning.llm_main import get_llm_review
from report.report_main import generate_markdown_report, save_report


def run(repo_path):
    files = find_python_files(repo_path)
    print(f"Found {len(files)} Python files.\n")

    all_results = []
    files_with_content = []

    for file_path in files:
        content = read_file_content(file_path)
        if content is None:
            continue

        files_with_content.append((file_path, content))

        ast_result = analyze_file(file_path, content)
        if ast_result is None:
            continue

        static_result = analyze_file_static(file_path)

        combined_result = {
            "file": file_path,
            "functions": ast_result["functions"],
            "classes": ast_result["classes"],
            "ruff_issues": static_result["ruff_issues"],
            "bandit_issues": static_result["bandit_issues"]
        }
        all_results.append(combined_result)

    graph = build_dependency_graph(files_with_content)

    print("Generating LLM review...\n")
    review = get_llm_review(all_results)

    report_content = generate_markdown_report(repo_path, all_results, graph, review)
    save_report(report_content)

    return all_results, graph, review
if __name__ == "__main__":
    repo_path = "."