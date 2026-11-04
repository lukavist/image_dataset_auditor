
from pathlib import Path
from image_auditor.models import ImageInspectionResult


def calculate_statistics(results: list[ImageInspectionResult], duplicates: list[list[Path]]):

    total_files = len(results)
    valid_images = 0
    invalid_images = 0
    file_size_in_bytes = 0

    formats: dict[str, int] = {}

    duplicate_groups = len(duplicates)
    duplicate_files = sum(len(group) for group in duplicates) 

    for res in results:
        
        if res.is_valid:
            valid_images += 1

            formats[res.image_format] = formats.get(res.image_format, 0) + 1
        else:
            invalid_images += 1

        file_size_in_bytes += res.file_path.stat().st_size


        
    total_size_mib = file_size_in_bytes / (1024 ** 2)

    return {
        'total_files': total_files,
        'valid_images': valid_images,
        'invalid_images': invalid_images,
        'total_size_mb': total_size_mib,
        'formats': formats,
        'duplicate_groups': duplicate_groups,
        'duplicate_files': duplicate_files
    }
