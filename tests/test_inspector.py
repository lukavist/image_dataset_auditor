from src.image_auditor.inspector import inspect_image
from PIL import Image
import pytest


def test_inspect_valid_image(tmp_path):
    d = tmp_path / 'inspector'
    d.mkdir()

    # create new Image
    im = Image.new('RGB', (100, 100))
    im.save(d / 'test_image.png')

    file_path = d / 'test_image.png'

    result = inspect_image(file_path)

    assert result.is_valid is True
    assert result.file_name == 'test_image.png'
    assert result.image_format == 'PNG'
    assert result.width == 100
    assert result.height == 100
    assert result.error is None


def test_inspect_corrupted_image(tmp_path):
    d = tmp_path / 'inspector'
    d.mkdir()
    # corrupted image
    with open(d / 'corrupted_image.png', 'wb') as f:
        f.write(b'not an image')

    file_path = d / 'corrupted_image.png'

    result = inspect_image(file_path)

    assert result.is_valid is False
    assert result.file_name == 'corrupted_image.png'
    assert result.error is not None


def test_inspect_nonexistent_file(tmp_path):
    d = tmp_path / 'inspector'
    d.mkdir()

    file_path = d / 'non_existent_image.png'
    with pytest.raises(FileNotFoundError):
        inspect_image(file_path)


def test_inspect_text_file(tmp_path):
    d = tmp_path / 'inspector'
    d.mkdir()

    # create a text file
    with open(d / 'test_file.jpg', 'w') as f:
        f.write('This is a text file.')

    file_path = d / 'test_file.jpg'

    result = inspect_image(file_path)

    assert result.is_valid is False
    assert result.file_name == 'test_file.jpg'
    assert result.error is not None