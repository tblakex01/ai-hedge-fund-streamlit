"""
Fix import statements in the AI Hedge Fund project.
This script updates import paths to use the correct 'src.' prefix.
"""
import os
import re

def fix_imports_in_file(file_path):
    """Update import statements in a single file to use 'src.' prefix."""
    print(f"Processing {file_path}...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # List of patterns to replace
        replacements = [
            ('from src.graph.state', 'from src.graph.state'),
            ('from src.tools.api', 'from src.tools.api'),
            ('from src.utils.progress', 'from src.utils.progress'),
            ('from src.utils.llm', 'from src.utils.llm'),
            ('from src.utils.display', 'from src.utils.display'),
            ('from src.utils.analysts', 'from src.utils.analysts'),
            ('from src.utils.visualize', 'from src.utils.visualize'),
            ('import src.agents.', 'import src.agents.'),
            ('from src.agents.', 'from src.agents.'),
            ('import src.graph.', 'import src.graph.'),
            ('from src.llm.', 'from src.llm.'),
            ('from src.graph.', 'from src.graph.'),
            ('from src.tools.', 'from src.tools.'),
            ('from src.main', 'from src.main'),
        ]
        
        # Apply each replacement pattern
        for old, new in replacements:
            if old in content:
                content = content.replace(old, new)
                print(f"  - Fixed: {old} -> {new}")
        
        # Write the updated content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Completed processing {file_path}")
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
    """Main function to fix imports throughout the project."""
    # Base directory containing the src folder
    base_dir = "d:\\ai_apps\\modelcontextprotocol\\testing\\ai-hedge-fund"
    src_dir = os.path.join(base_dir, "src")
    
    if not os.path.exists(src_dir):
        print(f"Error: Source directory not found: {src_dir}")
        return
    
    # Process all Python files in the src directory and its subdirectories
    process_directory(src_dir)
    
    print("\nImport statement update completed successfully.")

if __name__ == "__main__":
    main()
