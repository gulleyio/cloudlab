def main():
    print("Hello from collect-api-data!")


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


if __name__ == "__main__":
    main()
