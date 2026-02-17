import py_compile
import sys

try:
    py_compile.compile('github_job_fetcher.py', doraise=True)
    with open('syntax_check.txt', 'w') as f:
        f.write("Syntax OK")
except Exception as e:
    with open('syntax_check.txt', 'w') as f:
        f.write(f"Syntax Error: {e}")
