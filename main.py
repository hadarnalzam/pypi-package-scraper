import sys
from scraper.pipeline import scrape_package

import sys
from scraper.pipeline import scrape_package  # put your function in scraper/pipeline.py or __init__.py


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <package_name>")
        sys.exit(1)

    package_name = sys.argv[1]

    try:
        result = scrape_package(package_name)
        print("\n=== Results ===")
        print(f"Package: {result['package']}")
        print(f"Version: {result['version']}")
        print("Dependencies:")
        if result["dependencies"]:
            for dep in result["dependencies"]:
                print(f" - {dep}")
        else:
            print(" (none found)")
    except Exception as e:
        print(f"[ERROR] {str(e)}")


if __name__ == "__main__":
    main()
