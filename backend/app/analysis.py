import ast
from typing import List, Dict, Any

class CodeAnalyzer:
    def analyze_python(self, code: str) -> Dict[str, Any]:
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return {"error": "SyntaxError"}

        functions = []
        classes = []
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append({
                    "name": node.name,
                    "lineno": node.lineno,
                    "args": [arg.arg for arg in node.args.args]
                })
            elif isinstance(node, ast.ClassDef):
                classes.append({
                    "name": node.name,
                    "lineno": node.lineno
                })
            elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                # Simplified import extraction
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    for alias in node.names:
                        imports.append(f"{module}.{alias.name}")

        return {
            "functions": functions,
            "classes": classes,
            "imports": imports
        }

    def analyze(self, filename: str, content: str) -> Dict[str, Any]:
        if filename.endswith(".py"):
            return self.analyze_python(content)
        else:
            return {"message": "Unsupported file type for deep analysis"}
