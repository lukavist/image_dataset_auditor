
from pathlib import Path
import json
from image_auditor.models import ImageInspectionResult
import csv

def generate_report(results: list[ImageInspectionResult], duplicates: list[list[Path]], statistics: dict) -> dict:

    final_report = {}

    final_report['summary'] = statistics

    final_report['files'] = []
    final_report['duplicates'] = []

    for res in results:
        final_report['files'].append(
            {
                'file_name': res.file_name,
                'file_path': str(res.file_path),
                'format': res.image_format,
                'width': res.width,
                'height': res.height,
                'is_valid': res.is_valid,
                'error': res.error
            }
        )

    for dup in duplicates:
        final_report['duplicates'].append([str(path) for path in dup])

    return final_report


def save_json_report(report: dict, output_path: Path) -> None:
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)


def save_csv_report(report: dict, output_path: Path) -> None:
    # TODO: add check for empty report dict, and still write headers

    if not report['files']:
        report['files'].append({k: None for k in ['file_name', 'file_path', 'format', 'width', 'height', 'is_valid', 'error']})
    
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=report['files'][0].keys())
        writer.writeheader()
        for row in report['files']:
            writer.writerow(row)
