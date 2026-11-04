from pathlib import Path


def scan_directory(directory_path: Path) -> list[dict]:
    """
    Input: directory_path (Path) - the path to the directory to scan

    Raises:
        FileNotFoundError: If the directory does not exist
        NotADirectoryError: If the path is not a directory
        ValueError: If the directory is empty
    
    Output: List[dict] -  a list of files with info: file_path, file_name, extension
                        If result is empty return empty list
    """

    if not directory_path.exists():
        raise FileNotFoundError(f"{directory_path} does not exist")

    if not directory_path.is_dir():
        raise NotADirectoryError(f"{directory_path} is not a directory")

    files = directory_path.rglob('*')

    result = []

    for file in files:
        if file.is_file():
            result.append({
                "file_path": file,
                "file_name": file.name,
                "extension": file.suffix
            })

    return result


# print(scan_directory(Path('C:\\Users\\anton\\Desktop\\image_dataset_auditor\\src\\test_dataset')))
