# LESP

*Like lisp but way less.*

LESP is a simple variable arithmetic machine. You provide a lisp-like calculation string, and then provide the namespace mapping the variables to their numeric values and lesp does the rest.

Example:

Say you have code that calculates some percentage from census variables. This is how you would do that with LESP:


```python
from lesp import lexecute

lesp_string = "(* 100 (/ (+ B09019012 B09019013) B09019001))"


mi_namespace = {
    "B09019012": 10000,
    "B09019013": 12000,
    "B09019001": 27000,
}


result = lexecute(lesp_string, mi_namespace)
# .814814...
```

LESP works with any object that has all arithmetic dunder methods defined.

