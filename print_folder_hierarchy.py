import os
import argparse

# Predefined skip lists
DONT_SHOW = ['__pycache__']
DONT_SHOW_SUB_FILES = ['.git', 'venv', '.venv', '.pytest_cache']

def print_folder_hierarchy(startpath, dont_show, dont_show_sub_files):
    for root, dirs, files in os.walk(startpath, topdown=True):
        # Remove folders in DONT_SHOW from the traversal
        dirs[:] = [d for d in dirs if os.path.join(root, d) not in dont_show]
        
        level = root.replace(startpath, '').count(os.sep)
        indent = '│   ' * (level - 1) + '├── ' if level > 0 else ''
        print(f'{indent}{os.path.basename(root)}/')
        
        subindent = '│   ' * level + '├── '
        for f in files:
            print(f'{subindent}{f}')
        
        # Handle directories in DONT_SHOW_SUB_FILES
        for d in dirs[:]:  # Use a copy of dirs to modify the original list
            if os.path.join(root, d) in dont_show_sub_files:
                print(f'{subindent}{d}/')
                dirs.remove(d)

def main():
    parser = argparse.ArgumentParser(description='Print the folder hierarchy of a given directory, with options to skip specific folders.')
    parser.add_argument('--path', '-p', type=str, default=os.getcwd(), help='Specify the start path for the folder hierarchy. Uses the current working directory by default.')
    parser.add_argument('--use-current-dir', '-c', action='store_true', help='Use the current working directory as the start path')
    parser.add_argument('--skip', '-s', nargs='+', type=str, help='Folders to skip completely', default=[])
    parser.add_argument('--skip-sub-files', '-ssf', nargs='+', type=str, help='Folders to display but not their contents', default=[])
    parser.add_argument('--skip-list', '-l', action='store_true', help='Use the predefined skip list')

    args = parser.parse_args()
    
    # If --use-current-dir is specified, override the path with the current directory
    if args.use_current_dir:
        start_path = os.getcwd()
    else:
        start_path = args.path
    
    # Determine the skip lists to use
    if args.skip_list:
        dont_show = DONT_SHOW
        dont_show_sub_files = DONT_SHOW_SUB_FILES
    else:
        dont_show = args.skip
        dont_show_sub_files = args.skip_sub_files

    # Normalize paths to be absolute
    dont_show = [os.path.join(start_path, d) for d in dont_show]
    dont_show_sub_files = [os.path.join(start_path, d) for d in dont_show_sub_files]

    print_folder_hierarchy(start_path, dont_show, dont_show_sub_files)

if __name__ == '__main__':
    main()
