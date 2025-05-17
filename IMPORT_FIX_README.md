# AI Hedge Fund Import Fix Guide

## Issue Description

The AI Hedge Fund project encountered a module import error when running the Streamlit application:

```
ModuleNotFoundError: No module named 'data'
```

This error occurred because some import statements in the code were using relative imports without the proper `src.` prefix. Specifically, in `src/tools/api.py`, imports from the `data` module were not properly prefixed.

## Solution

Several scripts have been created to fix the import issues:

1. `fix_data_imports.py` - Specifically fixes imports from the `data` module
2. `fix_all_imports.py` - Comprehensive script to fix all import statements in the project
3. `test_imports.py` - Test script to verify that imports work correctly after fixing

## How to Fix the Import Issues

Follow these steps to fix the import issues:

1. Run the comprehensive fix script:

   ```bash
   python fix_all_imports.py
   ```

2. Test that the imports are now working correctly:

   ```bash
   python test_imports.py
   ```

3. If all tests pass, you can now run your Streamlit application:

   ```bash
   streamlit run app.py
   ```

## Alternative Method: Manual Fix

If the automated fix doesn't work, you can manually edit the `src/tools/api.py` file to change the following lines:

```python
from data.cache import get_cache
from data.models import (
    CompanyNews,
    CompanyNewsResponse,
    # ... other imports
)
```

to:

```python
from src.data.cache import get_cache
from src.data.models import (
    CompanyNews,
    CompanyNewsResponse,
    # ... other imports
)
```

## Python Module Structure

For reference, here's how imports should be structured in this project:

1. **Root-level scripts** (like `app.py`) should use imports prefixed with `src.`:
   ```python
   from src.main import run_hedge_fund
   from src.utils.analysts import ANALYST_ORDER
   ```

2. **Module-level scripts** (inside the `src` directory) should also use imports prefixed with `src.`:
   ```python
   from src.data.cache import get_cache
   from src.tools.api import get_prices
   ```

## Notes on Python Package Structure

This project follows a structure where all modules are imported from the project root, which is why all imports need to be prefixed with `src.`. This approach is convenient for running scripts from different locations but requires careful management of import statements.

For future development, consider setting up a proper Python package structure with `setup.py` or using `poetry` for dependency management, which would make import handling more robust.
