import json
from PIL import Image   
from image_auditor.models import ImageInspectionResult
from image_auditor.report_generator import generate_report, save_json_report
from image_auditor.statistics_calculator import calculate_statistics


def test_report_generator(tmp_path):
    results = []

    valid_paths = []
    for i in range(2):
        im = Image.new('RGB', (60, 80))
        file_path = tmp_path / f'image_{i}.png'
        im.save(file_path)
        valid_paths.append(file_path)

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

    bad_path = tmp_path / 'broken.txt'
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

    # identical images saved above form one duplicate group
    duplicates = [valid_paths]
    statistics = calculate_statistics(results, duplicates)

    report = generate_report(results, duplicates, statistics)

    assert set(report.keys()) == {'summary', 'files', 'duplicates'}
    assert report['summary'] == statistics

    assert len(report['files']) == 3
    expected_keys = {'file_name', 'file_path', 'format', 'width', 'height', 'is_valid', 'error'}
    for entry in report['files']:
        assert set(entry.keys()) == expected_keys

    first = report['files'][0]
    assert first['file_name'] == 'image_0.png'
    assert first['file_path'] == str(valid_paths[0])
    assert first['format'] == 'PNG'
    assert first['width'] == 60
    assert first['height'] == 80
    assert first['is_valid'] is True
    assert first['error'] is None

    invalid = report['files'][2]
    assert invalid['file_name'] == 'broken.txt'
    assert invalid['format'] is None
    assert invalid['width'] is None
    assert invalid['height'] is None
    assert invalid['is_valid'] is False
    assert invalid['error'] == 'Invalid Image'

    assert report['duplicates'] == [[str(p) for p in valid_paths]]


def test_empty_report(tmp_path):
    report = generate_report([], [], {})
    assert report['files'] == []
    assert report['duplicates'] == []
    assert report['summary'] == {}


def test_json_report(tmp_path):
    img_path = tmp_path / 'image.png'
    Image.new('RGB', (20, 30)).save(img_path)
    duplicate_path = tmp_path / 'image_copy.png'
    duplicate_path.write_bytes(img_path.read_bytes())
    bad_path = tmp_path / 'broken.txt'
    bad_path.write_text('not an image')

    results = [
        ImageInspectionResult(img_path, img_path.name, 'PNG', 20, 30, True, None),
        ImageInspectionResult(bad_path, bad_path.name, None, None, None, False, 'Invalid Image'),
    ]
    duplicates = [[img_path, duplicate_path]]
    statistics = calculate_statistics(results, duplicates)

    report = generate_report(results, duplicates, statistics)

    report_path = tmp_path / 'report.json'
    save_json_report(report, report_path)

    with open(report_path, encoding='utf-8') as f:
        loaded = json.load(f)

    assert report_path.exists()
    assert loaded == report