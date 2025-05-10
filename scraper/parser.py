import re
from pathlib import Path
from packaging.requirements import Requirement

def parse_dependencies(package_dir: str) -> list[str]:
    """
    Parse setup.py, requirements.txt, etc.
    Returns a list of dependency strings.
    """


    dependencies = set()

    # Try requirements.txt
    req_txt = list(Path(package_dir).rglob("requirements.txt"))
    if req_txt:
        with open(req_txt[0], "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    try:
                        dep = Requirement(line)
                        dependencies.add(str(dep))
                    except Exception:
                        pass  # Skip invalid lines

    setup_files = list(Path(package_dir).rglob("setup.py"))

    if setup_files:
        with open(setup_files[0], "r") as f:
            content = f.read()

            pattern = r'install_requires\s*=\s*\[(.*?)\]'
            match = re.search(pattern, content, re.DOTALL)

            if match:
                requires = match.group(1)
                deps = re.findall(r"'([^']+)'", requires)
                for dep in deps:
                    try:
                        dependencies.add(str(Requirement(dep)))
                    except Exception:
                        pass

    return sorted(dependencies)