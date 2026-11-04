from PIL import Image
from image_auditor.models import ImageInspectionResult
from image_auditor.statistics_calculator import calculate_statistics


def test_valid_results(tmp_path):
    d = tmp_path / 'valid_results'
    d.mkdir()

    results = []
    duplicated = []

    for i in range(4):

        im = Image.new('RGB', (120, 120))
        file_path = d / f'image_{i}.png'
        im.save(file_path)

        results.append(
            ImageInspectionResult(
                file_path=file_path,
                file_name=file_path.name,
                image_format=im.format,
                width=im.width,
                height=im.height,
                is_valid=True,
                error=None)
        )

    paper = calculate_statistics(results, duplicated)

    assert paper['total_files'] == 4
    assert paper['valid_images'] == 4
    assert paper['invalid_images'] == 0


def test_valid_invalid(tmp_path):
    d = tmp_path / 'results'
    d.mkdir()

    results = []
    duplicated = []

    # valid images
    for i in range(2):

        im = Image.new('RGB', (100, 120))
        file_path = d / f'valid_image_{i}.png'
        im.save(file_path)

        results.append(
            ImageInspectionResult(
                file_path=file_path,
                file_name=file_path.name,
                image_format=im.format,
                width=im.width,
                height=im.height,
                is_valid=True,
                error=None
            )
        )

    # invalid images (Text files)
    for i in range(2):
    
        with open(d /f'not_image_{i}.txt', 'w') as f:
            f.write(f'text_file {i}')
        file_path1 = d / f'not_image_{i}.txt'
        
        results.append(
            ImageInspectionResult(
                file_path=file_path1,
                file_name=file_path1.name,
                image_format=None,
                width=None,
                height=None,
                is_valid=False,
                error='Invalid Image'
            )
        )

    paper = calculate_statistics(results, duplicated)

    assert paper['total_files'] == 4
    assert paper['valid_images'] == 2
    assert paper['invalid_images'] == 2


def test_empty_results(tmp_path):
    results = []
    dupl = []

    paper = calculate_statistics(results, dupl)

    assert paper['total_files'] == 0
    assert paper['valid_images'] == 0
    assert paper['invalid_images'] == 0


def test_file_size(tmp_path):
    results = []
    expected_bytes = 0

    for i in range(2):
        im = Image.new('RGB', (50, 50))
        file_path = tmp_path / f'image_{i}.png'
        im.save(file_path)
        expected_bytes += file_path.stat().st_size

        results.append(
            ImageInspectionResult(
                file_path=file_path,
                file_name=file_path.name,
                image_format='PNG',
                width=im.width,
                height=im.height,
                is_valid=True,
                error=None
            )
        )

    for i in range(2):
        file_path = tmp_path / f'text_{i}.txt'
        file_path.write_text('some text ' * (i + 1))
        expected_bytes += file_path.stat().st_size

        results.append(
            ImageInspectionResult(
                file_path=file_path,
                file_name=file_path.name,
                image_format=None,
                width=None,
                height=None,
                is_valid=False,
                error='Invalid Image'
            )
        )

    paper = calculate_statistics(results, [])

    assert paper['total_files'] == 4
    assert paper['total_size_mb'] == expected_bytes / (1024 ** 2)


def test_formats_calculation(tmp_path):
    results = []

    for name, fmt, ext in [('a', 'JPEG', 'jpg'), ('b', 'JPEG', 'jpeg'), ('c', 'PNG', 'png')]:
        im = Image.new('RGB', (40, 40))
        file_path = tmp_path / f'{name}.{ext}'
        im.save(file_path, format=fmt)

        results.append(
            ImageInspectionResult(
                file_path=file_path,
                file_name=file_path.name,
                image_format=fmt,
                width=im.width,
                height=im.height,
                is_valid=True,
                error=None
            )
        )

    bad_path = tmp_path / 'broken.jpg'
    bad_path.write_text('not an image')
    results.append(
        ImageInspectionResult(
            file_path=bad_path,
            file_name=bad_path.name,
            image_format=None,
            width=None,
            height=None,
            is_valid=False,
            error='Invalid Image'
        )
    )

    paper = calculate_statistics(results, [])

    assert paper['formats'] == {'JPEG': 2, 'PNG': 1}
    assert paper['valid_images'] == 3
    assert paper['invalid_images'] == 1


def test_duplicate_info(tmp_path):
    results = []
    paths = []

    for i in range(5):
        im = Image.new('RGB', (30, 30), color=(i * 40, 0, 0))
        file_path = tmp_path / f'img_{i}.png'
        im.save(file_path)
        paths.append(file_path)

        results.append(
            ImageInspectionResult(
                file_path=file_path,
                file_name=file_path.name,
                image_format='PNG',
                width=im.width,
                height=im.height,
                is_valid=True,
                error=None
            )
        )

    # two groups: 3 files and 2 files
    duplicates = [paths[0:3], paths[3:5]]

    paper = calculate_statistics(results, duplicates)

    assert paper['duplicate_groups'] == 2
    assert paper['duplicate_files'] == 5


def test_no_duplicates(tmp_path):
    paper = calculate_statistics([], [])

    assert paper['duplicate_groups'] == 0
    assert paper['duplicate_files'] == 0