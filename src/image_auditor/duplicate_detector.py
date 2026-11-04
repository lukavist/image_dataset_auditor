import hashlib
from pathlib import Path
from image_auditor.models import ImageInspectionResult


def calculate_file_hash(file_path: Path) -> str:
    hasher = hashlib.sha256()
    buffer_size = 65536
    with file_path.open("rb") as f:
        while True:
            data = f.read(buffer_size)
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()


def find_duplicates(results: list[ImageInspectionResult]) -> list[list[Path]]:

    hash_map: dict[str, list[Path]] = {}

    for result in results:

        if result.is_valid:

            file_hash = calculate_file_hash(result.file_path)

            if file_hash not in hash_map:
                hash_map[file_hash] = []
            hash_map[file_hash].append(result.file_path)

        if not result.is_valid:
            continue

    duplicates = [paths for paths in hash_map.values() if len(paths) > 1]
    
    return duplicates


        