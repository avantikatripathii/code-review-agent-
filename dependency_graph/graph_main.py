import ast
import os
import networkx as nx


def extract_imports(file_path, content):
    """Parse a file and extract the names of modules it imports."""
    try:
        tree = ast.parse(content, filename=file_path)
    except SyntaxError:
        return []

    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

    return imports


def build_dependency_graph(files_with_content):
    """
    Build a graph where nodes are file paths and edges represent imports.
    files_with_content: list of (file_path, content) tuples
    """
    graph = nx.DiGraph()

    # map module names (like "parser.parser_main") to actual file paths
    module_to_file = {}
    for file_path, _ in files_with_content:
        rel_path = os.path.relpath(file_path).replace("\\", "/").replace(".py", "")
        module_name = rel_path.replace("/", ".")
        module_to_file[module_name] = file_path
        graph.add_node(file_path)

    for file_path, content in files_with_content:
        imports = extract_imports(file_path, content)
        for imp in imports:
            # only add edge if the import is one of OUR own files (not external libs)
            for module_name, target_file in module_to_file.items():
                if imp == module_name or module_name.startswith(imp + "."):
                    graph.add_edge(file_path, target_file)

    return graph


if __name__ == "__main__":
    from parser.parser_main import find_python_files, read_file_content

    files = find_python_files(".")
    files_with_content = [(f, read_file_content(f)) for f in files]
    files_with_content = [(f, c) for f, c in files_with_content if c is not None]

    graph = build_dependency_graph(files_with_content)

    print(f"Graph has {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges.\n")

    for source, target in graph.edges():
        print(f"  {source}  →  {target}")

    # check for circular dependencies
    cycles = list(nx.simple_cycles(graph))
    if cycles:
        print(f"\nWarning: {len(cycles)} circular dependency chain(s) found!")
        for cycle in cycles:
            print(f"  {' -> '.join(cycle)}")
    else:
        print("\nNo circular dependencies found.")