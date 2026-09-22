from parser.parser_main import find_python_files, read_file_content
from ast_analysis.ast_main import analyze_file
from static_analysis.static_main import analyze_file_static
from dependency_graph.graph_main import build_dependency_graph


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

        print(f"{file_path}")
        print(f"  Functions: {[f['name'] for f in combined_result['functions']]}")
        print(f"  Classes:   {[c['name'] for c in combined_result['classes']]}")
        print(f"  Ruff issues: {len(combined_result['ruff_issues'])}")
        print(f"  Bandit issues: {len(combined_result['bandit_issues'])}")

    # build dependency graph across all files
    graph = build_dependency_graph(files_with_content)
    print(f"\nDependency graph: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges")
    for source, target in graph.edges():
        print(f"  {source}  →  {target}")

    return all_results, graph


if __name__ == "__main__":
    repo_path = "."
    run(repo_path)