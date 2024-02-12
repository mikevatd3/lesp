# LESP

*Like lisp but way less.*

LESP is a simple variable arithmetic machine. You provide a lisp-like calculation string, and then provide the namespace mapping the variables to their numeric values and lesp does the rest.

*This is based heavily on Peter Norvig's python implementation of lisp found [here](https://norvig.com/lispy.html).*

Example:

Say you have code that calculates some percentage from census variables. This is how you would do that with LESP:


```python
from lesp import execute

lesp_string = "(* 100 (/ (+ B09019012 B09019013) B09019001))"


mi_namespace = {
    "B09019012": 10000,
    "B09019013": 12000,
    "B09019001": 27000,
}


result = execute(lesp_string, mi_namespace)
# .814814...
```

LESP works with any object that has all arithmetic dunder methods defined.

