from dataclasses import dataclass
from pathlib import Path


@dataclass
class ImageInspectionResult:
    file_path: Path
    file_name: str
    image_format: str | None
    width: int | None
    height: int | None
    is_valid: bool
    error: str | None
