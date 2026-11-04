
from pathlib import Path
from image_auditor.report_generator import generate_report, save_csv_report, save_json_report
from image_auditor.statistics_calculator import calculate_statistics
from image_auditor.auditor import audit_dataset
from image_auditor.duplicate_detector import find_duplicates

def auditor_pipeline(input_path: Path, output_path: Path) -> dict:
    """
    Audit dataset and generate report.
    input_path: path to image dataset
    output_path: directory where reports will be saved
    returns: audit results as dict
    """
    output_path.mkdir(parents=True, exist_ok=True)

    # Audit dataset
    results = audit_dataset(input_path)

    # Find duplicates
    duplicates = find_duplicates(results)

    # calculate statistics
    statistics = calculate_statistics(results, duplicates)

    # generate report
    report = generate_report(results, duplicates, statistics)

    # save reports
    save_json_report(report, output_path / "report.json")
    save_csv_report(report, output_path / "report.csv")

    return report

