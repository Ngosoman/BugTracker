import re

def analyze_python_code(code):
    """Basic Python code analysis"""
    issues = []
    lines = code.split('\n')
    
    for i, line in enumerate(lines, 1):
        line = line.strip()
        
        # Check for common issues
        if 'print ' in line and not line.startswith('#'):
            issues.append({
                'line_number': i,
                'issue_type': 'Python 2 Syntax',
                'description': 'print statement without parentheses',
                'severity': 'medium',
                'suggested_fix': f'Change to: print({line.split("print ")[1]})'
            })
        
        if ' == None' in line or ' != None' in line:
            issues.append({
                'line_number': i,
                'issue_type': 'None Comparison',
                'description': 'Use "is" or "is not" for None comparisons',
                'severity': 'low',
                'suggested_fix': line.replace(' == None', ' is None').replace(' != None', ' is not None')
            })
        
        
    
    return issues