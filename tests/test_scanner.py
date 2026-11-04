from pathlib import Path
from src.image_auditor.scanner import scan_directory

def test_scanner():
    file_path = Path('C:\\Users\\anton\\Desktop\\image_dataset_auditor\\src\\test_dataset')
    result = scan_directory(file_path)
    assert isinstance(result, list)