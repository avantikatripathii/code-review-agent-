import ast
import os


def find_test_files(repo_path):
    """Find files that look like test files."""
    test_files = []
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in ('venv', '__pycache__', '.git')]
        for file in files:
            if file.startswith('test_') or file.endswith('_test.py'):
                test_files.append(os.path.join(root, file))
    return test_files


def extract_tested_function_names(test_file_content):
    """
    Extract which function names are likely being tested,
    based on naming convention: test_<function_name>
    """
    try:
        tree = ast.parse(test_file_content)
    except SyntaxError:
        return set()

    tested = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
            tested.add(node.name[len("test_"):])
    return tested


def find_untested_functions(all_functions, tested_function_names):
    """
    all_functions: list of function names found across the repo (excluding test files)
    tested_function_names: set of function names that have a corresponding test
    """
    return [f for f in all_functions if f not in tested_function_names]


if __name__ == "__main__":
    from parser.parser_main import find_python_files, read_file_content

    repo_path = "."
    test_files = find_test_files(repo_path)
    print(f"Found {len(test_files)} test file(s): {test_files}\n")

    tested_names = set()
    for tf in test_files:
        content = read_file_content(tf)
        if content:
            tested_names |= extract_tested_function_names(content)

    print(f"Functions with tests: {tested_names if tested_names else 'None'}\n")

    # gather all function names from non-test files
    all_files = find_python_files(repo_path)
    all_function_names = []
    for f in all_files:
        if f in test_files:
            continue
        content = read_file_content(f)
        if content is None:
            continue
        try:
            tree = ast.parse(content)
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                all_function_names.append(node.name)

    untested = find_untested_functions(all_function_names, tested_names)
    print(f"Untested functions ({len(untested)}): {untested}")