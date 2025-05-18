# AGENTS.md

## Overview

This repository utilizes OpenAI Codex for AI-assisted development. The following guidelines ensure consistent code quality, testing standards, and seamless integration with Codex.

## Code Style

* Adhere to [PEP8](https://peps.python.org/pep-0008/) standards.
* Use [Black](https://black.readthedocs.io/en/stable/) for code formatting.
* Avoid abbreviations in variable and function names; use descriptive identifiers.

## Testing

* Write tests using [pytest](https://docs.pytest.org/en/stable/).
* Place all test files in the `tests/` directory.
* Ensure all tests pass before submitting a pull request.
* Use [flake8](https://flake8.pycqa.org/en/latest/) for linting; resolve all warnings and errors.

## Pull Request Instructions

* **Title Format**: `[Type] Short description`

  * Examples: `[Fix] Correct calculation error`, `[Feature] Add user authentication`
* **Description**:

  * **Summary**: Provide a brief overview of the changes.
  * **Testing Done**: Describe the tests performed and their outcomes.
* Link related issues using `Closes #issue_number`.