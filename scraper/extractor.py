import tarfile
import zipfile

def extract_distribution(file_path: str, extract_dir: str) -> None:
    """
    Extracts a .tar.gz or .whl/.zip file to a target directory.
    """
    if file_path.endswith(".tar.gz") or file_path.endswith(".tgz"):

        with tarfile.open(file_path, "r:gz") as tar:

            tar.extractall(path=extract_dir)

    elif file_path.endswith(".zip") or file_path.endswith(".whl"):

        with zipfile.ZipFile(file_path, 'r') as zip_ref:

            zip_ref.extractall(path=extract_dir)
    else:
        raise Exception("Unsupported file format for extraction")