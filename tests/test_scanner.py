from PIL import Image

from image_auditor.scanner import scan_directory


def test_scanner(tmp_path):
    d = tmp_path / 'dataset'
    d.mkdir()
    sub = d / 'nested'
    sub.mkdir()

    expected = {
        d / 'a.png': 'PNG',
        d / 'b.jpg': 'JPEG',
        sub / 'c.png': 'PNG',
        sub / 'd.jpg': 'JPEG',
    }
    for path, fmt in expected.items():
        Image.new('RGB', (30, 30)).save(path, format=fmt)

    result = scan_directory(d)

    assert isinstance(result, list)
    assert len(result) == 4
    assert {item['file_path'] for item in result} == set(expected)
    assert {item['file_name'] for item in result} == {'a.png', 'b.jpg', 'c.png', 'd.jpg'}
    assert {item['extension'] for item in result} == {'.png', '.jpg'}