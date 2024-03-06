import os
import argparse

# Predefined skip-list
PREDEFINED_SKIP_LIST = ['venv', '.git', '__pycache__']

def print_folder_hierarchy(startpath, skips):
    for root, dirs, files in os.walk(startpath, topdown=True):
        # Modify dirs in-place to skip unwanted folders
        dirs[:] = [d for d in dirs if d not in skips]
        
        level = root.replace(startpath, '').count(os.sep)
        indent = '│   ' * (level - 1) + '├── ' if level > 0 else ''
        print(f'{indent}{os.path.basename(root)}/')
        subindent = '│   ' * (level) + '├── '
        for f in files:
            print(f'{subindent}{f}')

def main():
    parser = argparse.ArgumentParser(description='Print the folder hierarchy of a given directory, with options to skip specific folders.')
    parser.add_argument('--path', '-p', type=str, default=os.getcwd(), help='Specify the start path for the folder hierarchy. Uses the current working directory by default.')
    parser.add_argument('--use-current-dir', '-c', action='store_true', help='Use the current working directory as the start path')
    parser.add_argument('--skip', '-s', nargs='+', type=str, help='Folders to skip', default=[])
    parser.add_argument('--skip-list', '-l', action='store_true', help='Use the predefined skip list')

    args = parser.parse_args()
    
    # If --use-current-dir is specified, override the path with the current directory
    if args.use_current_dir:
        start_path = os.getcwd()
    else:
        start_path = args.path
    
    # Determine the skip list to use
    if args.skip_list:
        skips = PREDEFINED_SKIP_LIST
    else:
        skips = args.skip

    print_folder_hierarchy(start_path, skips)

if __name__ == '__main__':
    main()
