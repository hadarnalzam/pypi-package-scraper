import requests

def get_latest_version_info(package_name: str) -> dict:
    """
    Fetch the latest version metadata from PyPI JSON API.
    Returns: {
        "version": "x.y.z",
        "urls": [...],  # list of files for this version
    }
    """

    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch package info for '{package_name}'")

    data = response.json()
    version = data["info"]["version"]
    urls = data["releases"][version]

    return version, urls