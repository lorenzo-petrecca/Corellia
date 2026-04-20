from pathlib import Path
import subprocess

from corellia.config import CorelliaConfig
from corellia import constants as cs


class PackageManager :
    def __init__(self, python_path: Path) -> None:
        self.python_path = python_path


    def ensure_python_exists(self) -> None:
        if not self.python_path.exists():
            raise FileNotFoundError(
                f"Python executable was not found in the virtual environment: {self.python_path}"
            )
            

    def install (self, project_dir: Path, deps: dict[str, str]) -> bool:
        self.ensure_python_exists()
    
        if not deps:
            return False
        
        packages = [f"{name}=={version}" for name, version in deps.items()]

        subprocess.run(
            [str(self.python_path), "-m", "pip", "install", *packages],
            cwd=project_dir,
            check=True
        )

        return True
    

    def _install_project_packages (
        self,
        project_dir: Path,
        group: dict[str, str],
        label: str,    
    ) -> list[str] :
        if group and self.install(project_dir=project_dir, deps=group) :
            return [
                f"Installed {len(group)} {label}:",
                *(f"- {name}@{version} --> installed" for name, version in group.items())
            ]

        return [f"Installed 0 {label}:"]



    def install_deps (self, project_dir: Path, config: CorelliaConfig) -> list[str]:
        return self._install_project_packages(
            project_dir,
            config.get_dependencies(),
            cs.DEPENDENCY_SECTION_NAME,
        )
        

    def install_dev_deps (self, project_dir: Path, config: CorelliaConfig) -> list[str]:
        return self._install_project_packages(
            project_dir,
            config.get_dev_dependencies(),
            cs.DEV_DEPENDENCY_SECTION_NAME,
        )
    

    def upgrade (self, project_dir) -> bool :
        self.ensure_python_exists()

        result = subprocess.run(
            [str(self.python_path), "-m", "pip", "install", "--upgrade", "pip"],
            cwd=project_dir,
            check=True
        )

        return result.returncode == 0

    

    def uninstall (self, project_dir: Path, package: str) -> bool :
        subprocess.run(
            [str(self.python_path), "-m", "pip", "uninstall", "-y", package],
            cwd=project_dir,
            check=True,
        )

        return True

