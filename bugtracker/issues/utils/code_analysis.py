import re
import openai
from django.conf import settings
from django.contrib import messages

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
            },
            {
                'pattern': r'import os|import sys',
                'type': 'Import Style',
                'description': 'Consider using specific imports instead of whole module',
                'severity': 'low',
                'fix': lambda l: l
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

def analyze_with_ai(code, language='python'):
    """
    Analyze code using OpenAI API (for advanced analysis)
    Requires: OPENAI_API_KEY in settings.py
    """
    try:
        # Get API key from settings
        api_key = getattr(settings, 'OPENAI_API_KEY', None)
        if not api_key:
            return {"error": "OpenAI API key not configured"}
        
        openai.api_key = api_key
        
        prompt = f"""
        Analyze this {language} code for bugs, security issues, and improvements:
        
        ```{language}
        {code}
        ```
        
        Provide analysis in this format:
        Line X: [Issue Type] - [Description] (Severity: [low/medium/high/critical])
        Suggested fix: [Fix suggestion]
        ---
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful code analysis assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.3
        )
        
        return {"analysis": response.choices[0].message.content}
        
    except Exception as e:
        return {"error": f"AI analysis failed: {str(e)}"}

def analyze_code(code, language='python', use_ai=False):
    """
    Main analysis function - chooses between basic and AI analysis
    """
    if use_ai:
        return analyze_with_ai(code, language)
    else:
        return analyze_python_code_basic(code)