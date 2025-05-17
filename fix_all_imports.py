"""
Fix all import statements in the AI Hedge Fund project to use proper src prefixes.

This script updates import paths for all modules to ensure they use the correct 'src.' prefix,
including data, agents, graph, tools, utils, and llm modules.
"""
import os
import re

def fix_imports_in_file(file_path):
    """Update import statements in a single file to use proper 'src.' prefixes."""
    print(f"Processing {file_path}...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # List of all module imports that need to be fixed
        replacements = [
            # Data module imports
            ('from src.data.cache', 'from src.data.cache'),
            ('from src.data.models', 'from src.data.models'),
            ('import src.data.', 'import src.data.'),
            ('from src.data.', 'from src.data.'),
            
            # Graph module imports
            ('from src.graph.state', 'from src.graph.state'),
            ('import src.graph.', 'import src.graph.'),
            ('from src.graph.', 'from src.graph.'),
            
            # Tools module imports
            ('from src.tools.api', 'from src.tools.api'),
            ('import src.tools.', 'import src.tools.'),
            ('from src.tools.', 'from src.tools.'),
            
            # Agents module imports
            ('import src.agents.', 'import src.agents.'),
            ('from src.agents.', 'from src.agents.'),
            
            # Utils module imports
            ('from src.utils.progress', 'from src.utils.progress'),
            ('from src.utils.llm', 'from src.utils.llm'),
            ('from src.utils.display', 'from src.utils.display'),
            ('from src.utils.analysts', 'from src.utils.analysts'),
            ('from src.utils.visualize', 'from src.utils.visualize'),
            ('import src.utils.', 'import src.utils.'),
            ('from src.utils.', 'from src.utils.'),
            
            # LLM module imports
            ('import src.llm.', 'import src.llm.'),
            ('from src.llm.', 'from src.llm.'),
            
            # Main module import
            ('from src.main', 'from src.main'),
            ('import src.main', 'import src.main'),
        ]
        
        # Apply each replacement pattern
        modified = False
        for old, new in replacements:
            if old in content:
                content = content.replace(old, new)
                print(f"  - Fixed: {old} -> {new}")
                modified = True
        
        if modified:
            # Write the updated content back to the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Completed processing {file_path} - imports fixed")
        else:
            print(f"No imports to fix in {file_path}")
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def process_directory(directory):
    """Process all Python files in the specified directory."""
    print(f"Processing directory: {directory}")
    
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        
        # Process Python files
        if os.path.isfile(item_path) and item.endswith('.py'):
            fix_imports_in_file(item_path)
        
        # Recursively process subdirectories
        elif os.path.isdir(item_path):
            process_directory(item_path)

def main():
    """Main function to fix all imports throughout the project."""
    # Base directory containing the src folder
    base_dir = "d:\\ai_apps\\modelcontextprotocol\\testing\\ai-hedge-fund"
    src_dir = os.path.join(base_dir, "src")
    
    if not os.path.exists(src_dir):
        print(f"Error: Source directory not found: {src_dir}")
        return
    
    # First fix the root app.py and other Python files in the base directory
    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        if os.path.isfile(item_path) and item.endswith('.py'):
            # These files should already have src. prefixed imports, but check anyway
            fix_imports_in_file(item_path)
    
    # Process all Python files in the src directory and its subdirectories
    process_directory(src_dir)
    
    # Double-check the api.py file since that's where the error was occurring
    api_path = os.path.join(src_dir, "tools", "api.py")
    if os.path.exists(api_path):
        print(f"\nSpecifically checking imports in {api_path}")
        fix_imports_in_file(api_path)
    
    print("\nImport statement update completed successfully.")

if __name__ == "__main__":
    main()
