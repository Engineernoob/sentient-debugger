import ast
from typing import List, Dict

class SecurityAnalyzer:
    def __init__(self):
        self.vulnerability_patterns = {
            'sql_injection': [
                'execute', 'executemany', 'raw', 'cursor.execute'
            ],
            'command_injection': [
                'os.system', 'subprocess.run', 'subprocess.Popen', 'eval', 'exec'
            ],
            'unsafe_deserialization': [
                'pickle.loads', 'yaml.load', 'eval', 'literal_eval'
            ]
        }
    
    def analyze_code(self, code: str) -> List[Dict]:
        """Analyze code for potential security vulnerabilities"""
        tree = ast.parse(code)
        vulnerabilities = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                self._check_call(node, vulnerabilities)
            elif isinstance(node, ast.Assign):
                self._check_assignment(node, vulnerabilities)
        
        return vulnerabilities
    
    def _check_call(self, node: ast.Call, vulnerabilities: List[Dict]):
        """Check function calls for potential vulnerabilities"""
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            for vuln_type, patterns in self.vulnerability_patterns.items():
                if func_name in patterns:
                    vulnerabilities.append({
                        'type': vuln_type,
                        'line': node.lineno,
                        'col': node.col_offset,
                        'description': f'Potentially unsafe {vuln_type} detected'
                    })