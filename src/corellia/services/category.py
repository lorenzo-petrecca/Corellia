from pathlib import Path
import shutil
import tomli_w

from corellia.config import CorelliaConfig
from corellia import constants as cs
from corellia.models import CATEGORIES
from corellia.services.scaffold import ScaffoldService, START_CODE_BLOCK, END_CODE_BLOCK


class CategoryService :
    def __init__(self, root: Path) -> None:
        self.root = root
        self.config = CorelliaConfig.load(self.root / cs.CORELLIA_CONFIG_FILE)
        self.category = self.config.get_project_category()
        self.project_name = self.config.get_project_name()
        

      

    def scaffold (self) -> None :
        if not self.category in CATEGORIES :
            raise ValueError(f"Unsupported category: {self.category}")

        if self.category == "package" :
            self._scaffold_package()
        elif self.category == "app" :
            self._scaffold_app()
        elif self.category == "deploy" :
            self._scaffold_deploy()

        self._create_readme()


    def _scaffold_package (self) -> None :
        module_path = self.root / "src" / self.project_name
        ScaffoldService.ensure_dir(module_path)
        ScaffoldService.write_file(
            module_path / "__init__.py",
            f'__version__ = {self.config.get_project_version()}',
            "",
        )

        tests_path = self.root / "tests"
        ScaffoldService.ensure_dir(tests_path)
        ScaffoldService.touch(tests_path / "__init__.py")

        

    def _scaffold_app (self) -> None :
        app_path = self.root / "app"
        ScaffoldService.write_file(
            self.root / "main.py",
            'def main() -> None:',
            START_CODE_BLOCK,
            'print("App started")',
            END_CODE_BLOCK,
            "",
            "",
            'if __name__ == "__main__":',
            START_CODE_BLOCK,
            'main()',
            END_CODE_BLOCK,
            indentation=4,
        )

        ScaffoldService.ensure_dir(app_path)
        ScaffoldService.touch(app_path / "__init__.py")

    def _scaffold_deploy (self) -> None :
        pass


    def _create_readme (self) -> None :
        ScaffoldService.from_template(self.root / "README.md", f"{str(self.category)}_README.txt")

    
    @staticmethod
    def init_package_build (root: Path) :
        config = CorelliaConfig.load(root / cs.CORELLIA_CONFIG_FILE)
        pyver = config.get_project_python_version()
        parts = pyver.split(".")
        major = int(parts[0])
        minor = int(parts[1])
        pyver_from = f">={pyver}"
        pyver_to = f"<{major}.{minor + 1}"
        data = {
            "build-system": {
                "requires": ["setuptools>=68", "wheel"],
                "build-backend": "setuptools.build_meta",
            },
            "project": {
                "name": config.get_project_name(),
                "version": config.get_project_version(),
                "description": "",
                "readme": "README.md",
                "requires-python": f"{pyver_from},{pyver_to}",
                "dependencies": [f"{name}=={version}" for name, version in config.get_dependencies().items()],
                "optional-dependencies": {
                    "dev": [f"{name}=={version}" for name, version in config.get_dev_dependencies().items()]
                },
            },
            "tool": {
                "setuptools": {
                    "package-dir": {"": "src"},
                    "packages": {
                        "find": {
                            "where": ["src"],
                        }
                    },
                }
            },
        }
        pyproject_path = root / "pyproject.toml"
        with pyproject_path.open('wb') as file :
            tomli_w.dump(data, file)



    def validate_layout (self) -> bool :
        if self.category == "package" :
            return self._validate_package()
        elif self.category == "app" :
            return self._validate_app()
        elif self.category == "deploy" :
            return self._validate_deploy()
        
        return False

    def _validate_package (self) -> bool :
        project_name = self.config.get_project_name()
        package_dir = self.root / "src" / project_name
        init_file = package_dir / "__init__.py"

        if not package_dir.exists() or not init_file.exists():
            return False
        
        return True

    def _validate_app (self) -> bool :
        return True
        
    def _validate_deploy (self) -> bool :
        return True
    


    def clean_build_artifacts(self) -> None:
        """
        Clean build artifacts before creating a new package build.

        Policy:
        - always remove build/
        - always remove *.egg-info
        - remove only dist artifacts matching the current project version
        """

        # 1. Remove build/
        shutil.rmtree(self.root / "build", ignore_errors=True)

        # 2. Remove *.egg-info directories/files in project root
        for path in self.root.glob("*.egg-info"):
            if path.is_dir():
                shutil.rmtree(path, ignore_errors=True)
            elif path.exists():
                path.unlink(missing_ok=True)

        # 3. Remove only current-version artifacts from dist/
        dist_dir = self.root / "dist"
        if not dist_dir.exists():
            return

        prefix = f"{self.project_name}-{self.config.get_project_version()}"

        for path in dist_dir.iterdir():
            if not path.is_file():
                continue

            if path.name.startswith(prefix):
                path.unlink(missing_ok=True)