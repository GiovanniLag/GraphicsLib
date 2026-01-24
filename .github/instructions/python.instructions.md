---
description: 'Python coding conventions and guidelines'
applyTo: '**/*.py'
---

# Python Coding Conventions

## Python Instructions

- Write clear and concise comments for each function.
- Ensure functions have descriptive names and include type hints.
- Provide docstrings following PEP 257 conventions.
- Use the `typing` module for type annotations (e.g., `List[str]`, `Dict[str, int]`).
- Break down complex functions into smaller, more manageable functions.

## Searching the web
- If the user asks for information that is not in your training data, search the web for relevant and up-to-date information.
- If explicitly asked to search the web do so.
- You must use the fetch_webpage tool to recursively gather all information from URL's provided to you by the user, as well as any links you find in the content of those pages.
- When searching the web, prioritize official documentation, reputable sources, and recent publications.
- When asked for best practices or guidelines, ensure that the information is current and widely accepted in the Python community by verifying with multiple sources.

## General Instructions

- Always prioritize readability and clarity.
- For algorithm-related code, include explanations of the approach used.
- Write code with good maintainability practices, including comments on why certain design decisions were made.
- Handle edge cases and write clear exception handling.
- For libraries or external dependencies, mention their usage and purpose in comments.
- Use consistent naming conventions and follow language-specific best practices.
- Write concise, efficient, and idiomatic code that is also easily understandable.

## Code Style and Formatting

- Follow the **PEP 8** style guide for Python.
- Maintain proper indentation (use 4 spaces for each level of indentation).
- Ensure lines do not exceed 79 characters.
- Place function and class docstrings immediately after the `def` or `class` keyword and use NumPy style.
- Use blank lines to separate functions, classes, and code blocks where appropriate.

## Edge Cases and Testing

- include test **only if required** by the user cases for critical paths of the application.
- Account for common edge cases like empty inputs, invalid data types, and large datasets.
- Include comments for edge cases and the expected behavior in those cases.
- Write unit tests for functions and document them with docstrings explaining the test cases.

## Example of Proper Documentation

```python
def calculate_area(radius: float) -> float:
    """
    Calculate the area of a circle given the radius.
    
    Parameters
    ----------
    radius : float
        The radius of the circle.
    
    Returns
    -------
    float
        The area of the circle, calculated as π * radius^2.
    """
    import math
    return math.pi * radius ** 2
```
