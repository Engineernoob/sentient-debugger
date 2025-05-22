from typing import Dict, List
import ast
import radon.metrics
import radon.complexity

class CodeQualityAnalyzer:
    def __init__(self):
        self.metrics_history = []
    
    def analyze_code(self, code: str) -> Dict:
        """Analyze code quality metrics"""
        tree = ast.parse(code)
        
        metrics = {
            'cyclomatic_complexity': self._calculate_complexity(code),
            'maintainability_index': radon.metrics.mi_visit(code, multi=True),
            'loc': len(code.splitlines()),
            'function_count': len([node for node in ast.walk(tree) 
                                 if isinstance(node, ast.FunctionDef)]),
            'class_count': len([node for node in ast.walk(tree) 
                              if isinstance(node, ast.ClassDef)])
        }
        
        self.metrics_history.append(metrics)
        return metrics
    
    def _calculate_complexity(self, code: str) -> float:
        """Calculate average cyclomatic complexity"""
        blocks = radon.complexity.cc_visit(code)
        if not blocks:
            return 0.0
        return sum(block.complexity for block in blocks) / len(blocks)