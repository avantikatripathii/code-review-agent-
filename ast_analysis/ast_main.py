import ast


def analyze_file(file_path, content):
    """Parse a Python file's content and extract basic structure info."""
    try:
        tree = ast.parse(content, filename=file_path)
    except SyntaxError as e:
        print(f"  Syntax error in {file_path}: {e}")
        return None

    functions = []
    classes = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append({
                "name": node.name,
                "line": node.lineno,
                "num_args": len(node.args.args)
            })
        elif isinstance(node, ast.ClassDef):
            classes.append({
                "name": node.name,
                "line": node.lineno
            })

    return {
        "file": file_path,
        "functions": functions,
        "classes": classes
    }


if __name__ == "__main__":
    # quick test on this file itself
    with open(__file__, "r", encoding="utf-8") as f:
        content = f.read()

    result = analyze_file(__file__, content)
    print(f"File: {result['file']}")
    print(f"Functions found: {len(result['functions'])}")
    for func in result['functions']:
        print(f"  - {func['name']} (line {func['line']}, {func['num_args']} args)")
    print(f"Classes found: {len(result['classes'])}")