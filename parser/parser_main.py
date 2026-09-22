import os


def find_python_files(repo_path):
    """Walk through a repo and return paths of all .py files."""
    python_files = []
    
    for root, dirs, files in os.walk(repo_path):
        # skip common folders we don't care about
        dirs[:] = [d for d in dirs if d not in ('venv', '__pycache__', '.git', 'node_modules')]
        
        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(root, file)
                python_files.append(full_path)
    
    return python_files


def read_file_content(file_path):
    """Read and return the content of a file, handling encoding issues."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except (UnicodeDecodeError, PermissionError) as e:
        print(f"  Skipped {file_path}: {e}")
        return None


if __name__ == "__main__":
    repo_path = "."
    files = find_python_files(repo_path)
    
    print(f"Found {len(files)} Python files:")
    for f in files:
        content = read_file_content(f)
        if content is not None:
            line_count = len(content.splitlines())
            print(f"  {f} ({line_count} lines)")