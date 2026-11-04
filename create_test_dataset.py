
import random
from pathlib import Path

from PIL import Image


def create_test_dataset(output_dir: Path = Path(__file__).parent / 'test_dataset') -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    rng = random.Random(42)

    # 12 valid images with unique colors/sizes, so only the explicit copies are duplicates
    valid_files = []
    for i in range(12):
        ext = 'png' if i % 2 == 0 else 'jpg'
        size = (rng.randint(50, 200), rng.randint(50, 200))
        color = (i * 20, rng.randint(0, 255), 255 - i * 20)
        file_path = output_dir / f'image_{i:02d}.{ext}'
        Image.new('RGB', size, color).save(file_path)
        valid_files.append(file_path)

    # text files disguised as images
    for i, ext in enumerate(['png', 'jpg', 'png']):
        (output_dir / f'fake_image_{i}.{ext}').write_text(f'this is not an image {i}')

    # truncated image data
    for i, ext in enumerate(['png', 'jpg', 'png']):
        data = valid_files[i].read_bytes()
        (output_dir / f'broken_{i}.{ext}').write_bytes(data[:len(data) // 3])

    # exact byte-for-byte copies
    for i in range(6):
        source = valid_files[i]
        copy = output_dir / f'copy_of_{source.name}'
        copy.write_bytes(source.read_bytes())

    return output_dir


if __name__ == '__main__':
    print(f'Dataset created at {create_test_dataset()}')