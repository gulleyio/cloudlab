filepath = "./data/servers.txt"
stripfilepath = "./data/strip_servers.txt"


def read_file(filepath: str) -> str:
    try:
        with open(filepath, "r") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        raise
    except PermissionError:
        print(f"Error: Permission denied to read '{filepath}'.")
        raise
    except OSError as e:
        print(f"Error: Failed to read '{filepath}': {e}")
        raise


def read_file_strip_empty_lines_and_skip_comments(filepath: str, stripfilepath: str):
    try:
        with open(filepath, "r") as file, open(stripfilepath, "w") as strip_file:
            for line in file:
                if line.strip():
                    strip_file.write(line)
    except FileNotFoundError:
        print("file not found")
        raise


def write_file(filepath: str, content: str) -> None:
    try:
        with open(filepath, "w") as file:
            file.write(content)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        raise
    except PermissionError:
        print(f"Error: Permission denied to write '{filepath}'.")
        raise
    except OSError as e:
        print(f"Error: Failed to write '{filepath}': {e}")
        raise


def parse_from_yaml_to_object():
    pass


def generate_report():
    pass


if __name__ == "__main__":
    content = read_file(filepath)
    print(content)

    stripped_content = read_file_strip_empty_lines_and_skip_comments(
        filepath, stripfilepath
    )
    print(stripped_content)
