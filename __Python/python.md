**pylint**

**pytest**

**flake8**

**pychecker**



    PyLint - Code quality/Error detection/Duplicate code detection
    pep8.py - PEP8 code quality
    pep257.py - PEP27 Comment quality
    
    
**pyflakes** - 

    Error detection
    Pyflakes only examines the syntax tree of each file individually. 
    That, combined with a limited set of errors, makes it faster than Pylint. 
    On the other hand, pyflakes is more limited in terms of the things it can check.


mccabe - Cyclomatic Complexity Analyser
dodgy - secrets leak detection
pyroma - setup.py validator
vulture - unused code detection
    
    While pyflakes doesn’t do any stylistic checks, 
    there is another tool that combines pyflakes with style checks against PEP8: Flake8. Flake8, aside from combining pyflakes and pep8, also adds per-project configuration ability.