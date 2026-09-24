# AI Code Review & Software Engineering Agent

An automated code review pipeline that goes beyond "paste code → get AI opinion." It analyzes a full Python repository through multiple structured stages before an LLM reasons over the findings — producing an explainable, PR-style review report.

## How it works
Git Repository
↓
Repository Parser → finds and reads all .py files
↓
AST Analysis → extracts functions, classes, structure
↓
Static Analysis → runs Ruff (linting) + Bandit (security)
↓
Dependency Graph → maps imports, detects circular dependencies
↓
LLM Reasoning (Groq) → summarizes findings into a PR-style review
↓
Report Generation → outputs a Markdown report

## Why this approach

Instead of dumping raw code into an LLM, each stage does what it's best at:
- Deterministic tools (AST, linters, security scanners) catch what they're reliable at
- The LLM only reasons over structured findings — prioritizing issues and suggesting fixes
- Every claim in the final report traces back to a specific tool, making the review explainable

## Tech stack

- **Python** — `ast` module for structural analysis
- **Ruff** — fast linting and style checks
- **Bandit** — security vulnerability scanning
- **NetworkX** — dependency graph construction and cycle detection
- **Groq API** (`openai/gpt-oss-20b`) — free LLM inference for review generation

## Setup

```bash
git clone <this-repo-url>
cd code-review-agent
python -m venv venv
venv\Scripts\Activate.ps1        # Windows
pip install -r requirements.txt
```

Create a `.env` file in the root with:
GROQ_API_KEY=your_key_here

## Usage

Edit `repo_path` in `run_pipeline.py` to point at any local repository, then run:

```bash
python run_pipeline.py
```

This generates `review_report.md` containing:
- Summary statistics (files analyzed, issues found)
- AI-generated PR-style review with severity ratings and fix suggestions
- Full dependency graph

## Sample output

Tested successfully on [psf/requests-html](https://github.com/psf/requests-html) — detected 58 style/compatibility issues via Ruff across 5 files, with zero security issues flagged by Bandit, and generated a structured AI review categorizing and prioritizing each finding.

## Project structure
code-review-agent/
├── parser/ # repository walking, file reading
├── ast_analysis/ # function/class extraction via AST
├── static_analysis/ # Ruff + Bandit wrappers
├── dependency_graph/ # import graph via NetworkX
├── llm_reasoning/ # Groq API integration
├── report/ # Markdown report generation
└── run_pipeline.py # orchestrates the full pipeline

## Future improvements

- Multi-language support via tree-sitter
- Test coverage integration (`coverage.py`)
- PDF/HTML report export
<!-- test change -->
