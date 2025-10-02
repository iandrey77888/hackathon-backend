import os

def generate_directory_tree(startpath, output_file, ignore_dirs=[".git", "__pycache__", "__pycache__", ".venv", "venv", ".vscode"]):
    with open(output_file, 'w', encoding='utf-8') as f:
        for root, dirs, files in os.walk(startpath):
            # Исключаем ненужные директории
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 2 * level
            f.write(f"{indent}{os.path.basename(root)}/\n")
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                if not file.endswith('.pyc'):  # Исключаем скомпилированные файлы Python
                    f.write(f"{subindent}{file}\n")

if __name__ == "__main__":
    project_root = os.path.dirname(os.path.abspath(__file__))
    output_filename = "project_structure.txt"
    generate_directory_tree(project_root, output_filename)
    print(f"Структура проекта записана в файл: {output_filename}")