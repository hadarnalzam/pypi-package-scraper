import os

from scraper.fetcher import get_latest_version_info
from scraper.downloader import download_distribution_file
from scraper.extractor import extract_distribution
from scraper.parser import parse_dependencies

def scrape_package(package_name):
    # Create persistent folder under current directory
    base_dir = os.path.join(os.getcwd(), f"{package_name}_folder")
    os.makedirs(base_dir, exist_ok=True)

    print(f"[INFO] Fetching latest version of '{package_name}'...")
    version, urls = fetch_latest_version(package_name)
    print(f"[INFO] Latest version: {version}")

    print(f"[INFO] Downloading package...")
    file_path = download_package(package_name, version, urls, base_dir)

    print(f"[INFO] Extracting package...")
    extract_to = os.path.join(base_dir, "extracted")
    os.makedirs(extract_to, exist_ok=True)
    extract_package(file_path, extract_to)

    print(f"[INFO] Extracting dependencies...")
    dependencies = extract_dependencies(extract_to)

    return {
        "package": package_name,
        "version": version,
        "dependencies": dependencies
    }