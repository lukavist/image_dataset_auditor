#import pytest
from PIL import Image
from image_auditor.duplicate_detector import find_duplicates
from image_auditor.models import ImageInspectionResult

def test_no_duplicates(tmp_path):
    d = tmp_path / 'valid_images'
    d.mkdir()

    im1 = Image.new('RGB', (100, 100))
    file_path = d / 'image1.jpg'
    im1.save(file_path)

    im2 = Image.new('RGB', (150, 100))
    file_path2 = d / 'image2.jpg'
    im2.save(file_path2)

    results = [
        ImageInspectionResult(file_name=file_path.name,
                              file_path=file_path,
                              image_format=im1.format,
                              width=im1.width,
                              height=im1.height,
                              is_valid=True,
                              error=None),
        ImageInspectionResult(file_name=file_path2.name,
                              file_path=file_path2,
                              image_format=im2.format,
                              width=im2.width,
                              height=im2.height,
                              is_valid=True,
                              error=None)
    ]

    duplicates = find_duplicates(results)
    assert duplicates == []


def test_find_duplicates(tmp_path):
    d = tmp_path / 'duplicated'
    d.mkdir()

    im1 = Image.new('RGB', (100, 100))
    file_path = d / 'image1.jpg'
    im1.save(file_path)

    file_path2 = d / 'image2.jpg'
    file_path2.write_bytes(file_path.read_bytes())

    results = [
        ImageInspectionResult(file_name=file_path.name,
                              file_path=file_path,
                              image_format=im1.format,
                              width=im1.width,
                              height=im1.height,
                              is_valid=True,
                              error=None),
        ImageInspectionResult(file_name=file_path2.name,
                              file_path=file_path2,
                              image_format=im1.format,
                              width=im1.width,
                              height=im1.height,
                              is_valid=True,
                              error=None)
    ]

    duplicates = find_duplicates(results)
    assert duplicates == [[file_path, file_path2]]


def test_skip_invalid_images(tmp_path):
    d = tmp_path / 'invalid_images'
    d.mkdir()

    for i in range(3):
        with open(d / f'image{i}.jpg', 'wb') as f:
            f.write(b'not an image')

    results = [
        ImageInspectionResult(file_name=f'image{i}.jpg',
                              file_path=d / f'image{i}.jpg',
                              image_format=None,
                              width=None,
                              height=None,
                              is_valid=False,
                              error="Invalid image")
        for i in range(3)
    ]

    duplicates = find_duplicates(results)
    assert duplicates == []

def test_empty_results():
    results = []
    duplicates = find_duplicates(results)
    assert duplicates == [] 