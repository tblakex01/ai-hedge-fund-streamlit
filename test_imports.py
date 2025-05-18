"""
Test script to verify that imports work correctly after fixing.
This script attempts to import key modules from the project to ensure they are accessible.
"""
import os
import sys
import traceback

def test_import(import_statement):
    """Test a single import statement."""
    try:
        exec(import_statement)
        print(f"✅ Successfully imported: {import_statement}")
        return True
    except Exception as e:
        print(f"❌ Failed to import: {import_statement}")
        print(f"   Error: {str(e)}")
        return False

def main():
    """Main function to test imports."""
    print("Testing imports for AI Hedge Fund project...\n")
    
    # Add the project root to Python path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if base_dir not in sys.path:
        sys.path.insert(0, base_dir)
        print(f"Added {base_dir} to Python path")
    
    # List of import statements to test
    import_statements = [
        # Test data module imports
        "from src.data.cache import get_cache",
        "from src.data.models import CompanyNews, FinancialMetrics",
        
        # Test tools module imports
        "from src.tools.api import get_prices, get_financial_metrics",
        
        # Test graph module imports (if available)
        "from src.graph.state import AgentState",
        
        # Test agents module imports (if available)
        "import src.agents",
        
        # Test main module import
        "from src.main import run_hedge_fund",
    ]
    
    # Test each import statement
    success_count = 0
    for stmt in import_statements:
        if test_import(stmt):
            success_count += 1
    
    # Print summary
    print(f"\nImport testing completed: {success_count}/{len(import_statements)} imports successful")
    if success_count == len(import_statements):
        print("\nAll imports working correctly!")
    else:
        failed = len(import_statements) - success_count
        print(f"\nWARNING: {failed} imports failed.")

if __name__ == "__main__":
    main()
