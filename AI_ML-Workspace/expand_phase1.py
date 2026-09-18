import re

filepath = r'd:\CodingSpace\Hashmil_Workspace\AI_ML-Workspace\AI_ML_Roadmap_Details.txt'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

replacement = """      - Basics
        - Variables
          - Naming Conventions (PEP 8)
          - Variable Assignment
          - Local vs Global Scope
          - global and nonlocal Keywords
        - Data Types
          - Numeric Types (int, float, complex)
          - Boolean (bool)
          - Sequence Types (str, list, tuple)
          - Set Types (set, frozenset)
          - Mapping (dict)
          - NoneType
        - Type Casting
          - Implicit Type Conversion
          - Explicit Type Casting (int(), float(), str(), list(), tuple(), set())
        - Input/Output
          - input() and print()
          - f-strings and String Formatting
          - File I/O Basics (open, read, write)
        - Operators
          - Arithmetic Operators
          - Comparison Operators
          - Logical Operators (and, or, not)
          - Bitwise Operators
          - Assignment Operators
          - Identity Operators (is, is not)
          - Membership Operators (in, not in)
        - Mutable vs Immutable
          - Memory Address (id())
          - Mutable Types (List, Dict, Set)
          - Immutable Types (Int, Float, String, Tuple)
        - Memory management
          - Reference counting
          - Garbage Collection module (gc)
          - Memory Leaks in Python
      - Data Structures
        - Strings (Regex)
          - Slicing and Indexing
          - String Methods (split, join, replace, strip)
          - Regular Expressions (re module)
        - Lists
          - List Comprehensions
          - List Methods (append, extend, pop, insert, sort)
          - Deep Copy vs Shallow Copy
        - Tuples
          - Tuple Packing and Unpacking
          - NamedTuples
        - Sets
          - Set Operations (Union, Intersection, Difference)
          - Set Comprehensions
        - Dictionaries
          - Dictionary Comprehensions
          - Dictionary Methods (keys, values, items, get)
          - DefaultDict
          - OrderedDict
          - Counter
      - Conditions
        - if
          - Syntax and Indentation
          - Nested if statements
        - elif
          - Multi-way branching
        - else
          - Default condition execution
          - else with loops
        - Ternary Operators
          - One-line conditionals
        - match case
          - Structural Pattern Matching (Python 3.10+)
      - Loops & Iteration
        - for loop
          - Iterating over sequences
          - Enumerate and Zip
        - while loop
          - Infinite loops
          - Break and Continue
        - enumerate()
          - Index tracking
        - zip()
          - Parallel iteration
        - range()
          - Generating sequences
        - Iterators
          - __iter__ and __next__
        - Iterable Protocol
        - Generators
          - yield keyword
        - Async Generators
    - Functions & Advanced Concepts
      - Functions
        - Positional & Keyword Arguments
        - Lambda Functions
        - Recursion
        - Type Hinting (Generics, Protocols)
        - Docstrings
        - Built-in Functions
        - args & kwargs
        - Lambdas
        - Iterators
        - Generator Expressions
        - Regular Expressions
      - Functional Programming
        - map
        - filter"""

# Find the start and end precisely using string index
start_marker = "      - Basics"
end_marker = "      - Functional Programming\n        - map\n        - filter"
start_idx = content.find(start_marker, content.find("### PHASE 1: Python Deep Dive"))
end_idx = content.find(end_marker, start_idx) + len(end_marker)

if start_idx != -1 and end_idx != -1:
    new_content = content[:start_idx] + replacement + content[end_idx:]
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Replaced Phase 1 successfully!")
else:
    print(f"Failed to find indices. Start: {start_idx}, End: {end_idx}")
