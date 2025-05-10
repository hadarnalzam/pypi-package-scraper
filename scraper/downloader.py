import os
import requests


def download_distribution_file(urls: list, dest_dir: str) -> str:
    """
    Download a .tar.gz or .whl file from the given URLs.
    Returns path to the downloaded file.
    """

    priority = [".tar.gz", ".whl", ".zip"]

    # Sort urls by priority
    def get_priority(filename):
        for i, ext in enumerate(priority):
            if filename.endswith(ext):
                return i
        return len(priority)  # lowest priority if not matched

    sorted_urls = sorted(urls, key=lambda x: get_priority(x["filename"]))

    for file_info in sorted_urls:
        file_url = file_info["url"]
        file_name = file_info["filename"]

        response = requests.get(file_url, stream=True)

        if response.status_code == 200:
            local_file = os.path.join(dest_dir, file_name)
            with open(local_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return local_file

        elif 400 <= response.status_code < 500:
            raise Exception(f"Client error {response.status_code} when accessing: {file_url}")

    raise Exception("Could not download any valid distribution file.")