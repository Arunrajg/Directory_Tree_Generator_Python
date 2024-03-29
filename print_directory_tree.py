from pathlib import Path
import os

spaces = "   "
branch = "|  "
tee = "|--"
last = "|__"


def default_criteria(path: Path):
    ignore_list = [".git", "Docs"]
    return path.name not in ignore_list


def make_tree(root: str, level: int = -1, directories_only: bool = False, criteria: object = None):
    files = 0
    directories = 0
    file_extension = {}
    root = Path(str(root))
    if not criteria:
        criteria = default_criteria

    def inner(root: Path, level: int = level, prefix: str = ""):
        nonlocal files, directories, file_extension
        if not level:
            return
        if directories_only:
            contents = [d for d in root.iterdir() if d.is_dir()]
        else:
            contents = list(root.iterdir())
        contents = sorted(list(filter(criteria, contents)),
                          key=lambda k: str(k.name).lower())
        pointers = [tee] * (len(contents) - 1) + [last]
        for pointer, content in zip(pointers, contents):
            if content.is_dir():
                yield prefix+pointer+content.name+"/"
                directories += 1
                extension = branch if pointer is tee else spaces
                yield from inner(content, level=level-1, prefix=prefix+extension)
            elif not directories_only:
                files += 1
                file_suffix = content.suffix
                if not file_suffix:
                    file_suffix = "no_extension"
                if file_suffix in file_extension:
                    file_extension[file_suffix] += 1
                else:
                    file_extension[file_suffix] = 1
                yield prefix + pointer + content.name
    tree = [root.name+"/"] + list(inner(root, level)) + [f"Total {directories} directories, {files} files"] + ["\n"] + [
        f"{ext} = {num} files" for ext, num in file_extension.items()]
    return tree


def print_tree(input_folder: str, level=-1, directory_only=False):
    paths = make_tree(input_folder, level, directory_only)
    output_file = f"{input_folder}/tree_structure.txt"
    if os.path.exists(output_file):
        os.remove(output_file)
    for path in paths:
        with open(output_file, "a") as f:
            f.write(path)
            f.write("\n")
    print(f"created tree file {output_file}")


if __name__ == "__main__":
    input_path = input("Enter Input Folder: ")
    nested_level = input("Enter num of levels(Default:All): ")
    directories_only = input("Do you want to print only directories(y/n)? ")
    try:
        level = int(nested_level)
    except Exception:
        level = -1
    directory_only = directories_only.lower() == 'y'
    print_tree(input_path, level, directory_only)
