"""
Fix data module import statements in the AI Hedge Fund project.
This script updates import paths to use the correct 'src.data' prefix.
"""
import os
import re

def fix_imports_in_file(file_path):
    """Update import statements in a single file to use 'src.data' prefix."""
    print(f"Processing {file_path}...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Specific patterns for data module imports
        replacements = [
            ('from src.data.cache', 'from src.data.cache'),
            ('from src.data.models', 'from src.data.models'),
            ('import src.data.', 'import src.data.'),
            ('from src.data.', 'from src.data.'),
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
            print(f"No data imports to fix in {file_path}")
            
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
    """Main function to fix data imports throughout the project."""
    # Base directory containing the src folder
    base_dir = "d:\\ai_apps\\modelcontextprotocol\\testing\\ai-hedge-fund"
    src_dir = os.path.join(base_dir, "src")
    
    if not os.path.exists(src_dir):
        print(f"Error: Source directory not found: {src_dir}")
        return
    
    # Process all Python files in the src directory and its subdirectories
    process_directory(src_dir)
    
    # Specifically fix the api.py file since that's where the error is occurring
    api_path = os.path.join(src_dir, "tools", "api.py")
    if os.path.exists(api_path):
        print(f"\nSpecifically fixing imports in {api_path}")
        fix_imports_in_file(api_path)
    
    print("\nData import statement update completed successfully.")

if __name__ == "__main__":
    main()
