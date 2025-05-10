# PyPI Package Scraper

A Python CLI tool to fetch the latest version of a PyPI package, download its source code archive, and extract a list of its dependencies.

## 📦 Features

- Get the latest release metadata from PyPI
- Download `.tar.gz` or `.whl` source distributions
- Extract package contents to a local folder
- Parse dependencies from:
  - `requirements.txt`
  - `setup.py`

## 🚀 Usage

```bash
python main.py <package_name>
