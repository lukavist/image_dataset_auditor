# Image Dataset Auditor

A lightweight Python tool for auditing image datasets.

Image Dataset Auditor scans image directories, checks image validity, extracts metadata, detects exact duplicate files, calculates dataset statistics, and generates JSON and CSV reports

## Features

- **Recursive directory scanning** - scans all files in the specified directory and its subdirectories.
- **Image validation** - detects corrupted images and non-image files with image extensions.
- **Metadata extraction** - retrieves image format, width, and height.
- **Exact duplicate detection** - identifies byte-identical files using SHA-256 hashes.
- **Dataset statistics** - calculates total file count, valid and invalid image counts, format distribution, total dataset size, and duplicate statistics.
- **Report generation** - exports audit results to JSON and CSV formats.
- **Command-line interface (CLI)** - allows users to audit datasets directly from the terminal.

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd image_dataset_auditor
   ```

2. Create a virtual environment:

   ```python
   python -m venv .venv
   ```

3. Activate the virtual environment:

   Windows:
   ```bash
   .venv\Scripts\activate
   ```

   Linux/macOS:
   ```bash
   source .venv/bin/activate
   ```

4. Install the package:

   ```python
   python -m pip install -e .
   ```

## Usage

Run the auditor by specifying the path to your image dataset:

```bash
image-auditor ./dataset
```

By default, reports are saved to the `./reports` directory.

To specify a custom output directory:

```bash
image-auditor ./dataset --output ./my_reports
```

To display available command-line arguments:

```bash
image-auditor --help
```

## Output

The auditor generates two reports in the specified output directory:

- `report.json` — detailed audit results, including summary statistics, individual file metadata, validation status, errors, and duplicate groups.
- `report.csv` — tabular file-level audit results that can be opened in spreadsheet applications.

The JSON report contains three main sections:

- `summary` — overall dataset statistics.
- `files` — metadata and validation results for each scanned file.
- `duplicates` — groups of byte-identical files.

Example terminal output:

```text
Total_files: 24
Invalid_images: 6
Valid_images: 18
Report saved to: reports
```

## Project Structure

```text
image_dataset_auditor/
├── src/
│   └── image_auditor/
│       ├── __init__.py
│       ├── cli.py                   # Command-line interface
│       ├── auditor_pipeline.py      # Runs the full audit
│       ├── scanner.py               # Recursive file scanning
│       ├── inspector.py             # Image validation and metadata
│       ├── duplicate_detector.py    # SHA-256 duplicate detection
│       ├── statistics_calculator.py # Dataset statistics
│       ├── report_generator.py      # JSON and CSV reports
│       └── models.py                # Data models
├── tests/                           # Unit tests
├── create_test_dataset.py           # Generates a sample dataset
├── pyproject.toml
└── README.md
```

## Limitations

- **Exact duplicate detection only** — identifies byte-identical files using SHA-256 hashes. It does not detect visually similar images, resized copies, or re-encoded versions.
- **Read-only operation** — does not modify, move, or delete source files. Invalid files and duplicates must be handled manually.
- **Local datasets only** — currently supports local directory-based datasets. Remote storage and archive files are not supported.
- **No semantic image analysis** — does not perform image classification or content recognition. Validation is limited to file integrity and basic metadata extraction (format, width, and height).
- **No historical comparison** — each audit generates an independent report. Results from previous audits are not stored or compared automatically.

## Future Improvements

## Future Improvements

The following features are planned for future releases:

- **Perceptual duplicate detection** — implement perceptual hashing to identify visually similar images, including resized, compressed, or slightly modified versions of the same image.

- **Configurable image requirements** — allow users to define minimum and maximum image dimensions, supported formats, aspect ratios, and file size limits.

- **HTML reports** — generate interactive HTML reports with visual summaries, statistics, image previews, and detailed validation results.

- **Dataset class distribution analysis** — analyze class distribution in labeled datasets to identify class imbalance and underrepresented categories.

- **Train/validation/test leakage detection** — identify potential data leakage caused by identical or visually similar images appearing across different dataset splits.

- **Cloud storage support** — extend dataset scanning to support remote storage services such as Amazon S3 and other S3-compatible storage providers.

- **Historical audit comparison** — store previous audit results and compare them over time to track dataset changes, detect newly introduced issues, and monitor data quality.