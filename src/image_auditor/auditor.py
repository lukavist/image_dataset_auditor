from pathlib import Path
from image_auditor.inspector import ImageInspectionResult, inspect_image
from image_auditor.scanner import scan_directory

def audit_dataset(directory_path: Path) -> list[ImageInspectionResult]:

    files = scan_directory(directory_path)

    results: list[ImageInspectionResult] = []

    for file in files:
        result = inspect_image(file['file_path'])
        results.append(result)

    return results