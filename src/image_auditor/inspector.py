from PIL import Image
from pathlib import Path
from image_auditor.models import ImageInspectionResult


def inspect_image(file_path: Path) -> ImageInspectionResult:
    """
    Input: recieves a file path to an image as a Path object.
    Output: returns an ImageInspectionResult indicating the result of the inspection.
    """

    if not file_path.exists():
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    if not file_path.is_file():
        raise ValueError(f"The path {file_path} is not a file.")

    file_name = file_path.name

    try:
        with Image.open(file_path) as im:
            im.verify()

        with Image.open(file_path) as img:

            img.load()

            image_format = img.format
            image_height = img.height
            image_width = img.width

        if image_format is not None and image_height is not None and image_width is not None:
            return ImageInspectionResult(
                file_path=file_path,
                file_name=file_name,
                is_valid=True,
                error=None,
                image_format=image_format,
                height=image_height,
                width=image_width
            )
    except OSError as e:
        return ImageInspectionResult(
            file_path=file_path,
            file_name=file_name,
            is_valid=False, 
            image_format=None,
            width=None,
            height=None,
            error=str(e)
        )
