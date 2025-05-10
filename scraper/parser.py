import re
from pathlib import Path
from packaging.requirements import Requirement

# For TOML parsing: use tomllib (Python 3.11+) or fallback to tomli
try:
    import tomllib  # Python 3.11+
except ImportError:
    import tomli as tomllib  # Requires: pip install tomli

def parse_dependencies(package_dir: str) -> list[str]:
    """
    Extracts dependencies from:
    - requirements.txt
    - setup.py
    - .dist-info/METADATA
    - pyproject.toml
    Returns a sorted list of dependency strings.
    """
    dependencies = set()

    # --- 1. requirements.txt ---
    for req_file in Path(package_dir).rglob("requirements.txt"):
        with open(req_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    try:
                        dependencies.add(str(Requirement(line)))
                    except Exception:
                        pass

    # --- 2. setup.py ---
    for setup_file in Path(package_dir).rglob("setup.py"):
        with open(setup_file, "r", encoding="utf-8") as f:
            content = f.read()
            match = re.search(r'install_requires\s*=\s*\[(.*?)]', content, re.DOTALL)
            if match:
                requires = match.group(1)
                deps = re.findall(r"['\"]([^'\"]+)['\"]", requires)
                for dep in deps:
                    try:
                        dependencies.add(str(Requirement(dep)))
                    except Exception:
                        pass

    # --- 3. .dist-info/METADATA ---
    for metadata_file in Path(package_dir).rglob("*.dist-info/METADATA"):
        with open(metadata_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("Requires-Dist:"):
                    dep = line[len("Requires-Dist:"):].strip()
                    try:
                        dependencies.add(str(Requirement(dep)))
                    except Exception:
                        pass

    # --- 4. pyproject.toml ---
    for pyproject_file in Path(package_dir).rglob("pyproject.toml"):
        try:
            with open(pyproject_file, "rb") as f:
                toml_data = tomllib.load(f)
                project = toml_data.get("project", {})
                deps = project.get("dependencies", [])
                for dep in deps:
                    try:
                        dependencies.add(str(Requirement(dep)))
                    except Exception:
                        pass
        except Exception:
            pass  # Invalid TOML or structure

    return sorted(dependencies)
