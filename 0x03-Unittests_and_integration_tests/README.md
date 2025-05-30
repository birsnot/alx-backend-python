# 0x03. Unittests and Integration Tests

This project focuses on writing unit and integration tests in Python. It covers the use of the `unittest` module, parameterized testing, and mocking.

## Learning Objectives

- Understand the difference between unit and integration tests
- Know how to test code using Python's built-in `unittest` module
- Use `parameterized` to test functions with multiple inputs
- Mock external APIs or parts of a system to isolate tests
- Understand and implement test-driven development (TDD)

## Project Structure

- `utils.py`: Contains utility functions to be tested, such as `access_nested_map`, `get_json`, and `memoize`.
- `test_utils.py`: Contains the unit tests for `utils.py` using the `unittest` framework.
- Other test files: Will contain additional tests for different parts of the codebase.

## Requirements

- All Python files are interpreted/compiled with Python 3.7 on Ubuntu 18.04 LTS
- All files end with a new line
- The first line of each file is: `#!/usr/bin/env python3`
- Code follows `pycodestyle` (version 2.5)
- All files are executable
- Modules, classes, and functions include full docstrings
- All functions and coroutines use type annotations

## How to Run Tests

You can run all the tests with:

```bash
python3 -m unittest discover
```

Or to run a specific test file:

```bash
python3 -m unittest test_utils.py
```

## Installation

Install test dependencies with:

```bash
pip install parameterized
```