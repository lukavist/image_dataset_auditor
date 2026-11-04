import pytest
from PIL import Image
from src.image_auditor.auditor import audit_dataset


def test_valid_directory(tmp_path):
    d = tmp_path / 'auditor'
    d.mkdir()

    # create valid image
    im = Image.new('RGB', (100, 100))
    im.save(d / 'test_image.png')

    # create text-file
    with open(d / 'test_file.txt', 'w') as f:
        f.write('This is a text file.')
    
    results_by_name = {result.file_name: result for result in audit_dataset(d)}


    assert results_by_name['test_image.png'].is_valid is True
    assert results_by_name['test_image.png'].file_name == 'test_image.png'
    assert results_by_name['test_file.txt'].is_valid is False
    assert results_by_name['test_file.txt'].file_name == 'test_file.txt'
    assert results_by_name['test_file.txt'].error is not None


def test_empty_directory(tmp_path):
    d = tmp_path / 'auditor'
    d.mkdir()

    results = audit_dataset(d)

    assert results == []

def test_non_existent_directory(tmp_path):
    d = tmp_path / 'non_existent'

    with pytest.raises(FileNotFoundError):
        audit_dataset(d)