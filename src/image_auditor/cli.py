from pathlib import Path
import argparse
from image_auditor.auditor_pipeline import auditor_pipeline

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Path to input dataset")
    parser.add_argument("--output", help="Path to output", default="./reports")

    args = parser.parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)
    try:
        report = auditor_pipeline(input_path, output_path)
    except (FileNotFoundError, NotADirectoryError) as e:
        print(f"Error: {e}")
        return 
    
    print(f"Total_files: {report['summary'].get('total_files')}")

    print(f"Invalid_images: {report['summary'].get('invalid_images')}")

    print(f"Valid_images: {report['summary'].get('valid_images')}")

    print(f"Report saved to: {output_path}")


if __name__ == "__main__":
    main()