from parser.parser_main import find_python_files, read_file_content
from ast_analysis.ast_main import analyze_file


def run(repo_path):
    files = find_python_files(repo_path)
    print(f"Found {len(files)} Python files.\n")

    all_results = []

    for file_path in files:
        content = read_file_content(file_path)
        if content is None:
            continue

        result = analyze_file(file_path, content)
        if result is None:
            continue

        all_results.append(result)

        print(f"{file_path}")
        print(f"  Functions: {[f['name'] for f in result['functions']]}")
        print(f"  Classes:   {[c['name'] for c in result['classes']]}")

    return all_results


if __name__ == "__main__":
    repo_path = "."
    run(repo_path)