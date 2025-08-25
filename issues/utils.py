import re
import openai
from django.conf import settings

def analyze_python_code_basic(code):
    """
    Basic Python code analysis using pattern matching
    Returns: list of issues found
    """
    issues = []
    lines = code.split('\n')
    
    for i, line in enumerate(lines, 1):
        line = line.strip()
        
        # Skip empty lines and comments
        if not line or line.startswith('#'):
            continue
            
        # Check for common Python issues
        checks = [
            {
                'pattern': r'print\s+[^\(]',
                'type': 'Python 2 Syntax',
                'description': 'print statement without parentheses',
                'severity': 'medium',
                'fix': lambda l: re.sub(r'print\s+([^\(].*)', r'print(\1)', l)
            },
            {
                'pattern': r'==\s*None|\!=\s*None',
                'type': 'None Comparison',
                'description': 'Use "is" or "is not" for None comparisons',
                'severity': 'low',
                'fix': lambda l: l.replace(' == None', ' is None').replace(' != None', ' is not None')
            },
            {
                'pattern': r'except:',
                'type': 'Bare Except',
                'description': 'Bare except clause - specify exception type',
                'severity': 'medium',
                'fix': lambda l: l.replace('except:', 'except Exception:')
            }
        ]
        
        for check in checks:
            if re.search(check['pattern'], line):
                issues.append({
                    'line_number': i,
                    'issue_type': check['type'],
                    'description': check['description'],
                    'severity': check['severity'],
                    'suggested_fix': check['fix'](line),
                    'original_line': line
                })
                break
    
    return issues

def analyze_code(code, language='python', use_ai=False):
    """
    Main analysis function - uses basic analysis for now
    """
    if language == 'python':
        return analyze_python_code_basic(code)
    else:
        return []