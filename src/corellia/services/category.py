from pathlib import Path
import shutil
import tomli_w
from packaging.utils import canonicalize_name

from corellia.config import CorelliaConfig, default_module_name
from corellia import constants as cs
from corellia.models import CATEGORIES, Category
from corellia.services.scaffold import ScaffoldService, START_CODE_BLOCK, END_CODE_BLOCK
from corellia.utils.file_io import write_text


class CategoryService :
    def __init__(self, root: Path) -> None:
        self.root = root
        self.config = CorelliaConfig.load(self.root / cs.CORELLIA_CONFIG_FILE)
        self.category = self.config.project.category
        self.project_name = self.config.project.name
        

    def get_module_name (self) -> str :
        module = self.config.project.module
        if module :
            return module
        if self.category in CATEGORIES:
            category: Category = self.category
        else :
            category = "package"

        return default_module_name(
            self.config.project.name,
            category,
        )

    def get_module_path (self) -> Path :
        """
        Ritorna il path della cartella modulo (varia a seconda della categoria)
        """
        module = self.get_module_name()

        if self.category in CATEGORIES :
            match self.category :
                case "package" :
                    return self.root / "src" / module
                case "app" | "deploy":
                    return self.root / module

        raise ValueError(
            f"Unsupported project category: {self.category}"
        )
      

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
        module_path = self.get_module_path()
        ScaffoldService.ensure_dir(module_path)
        ScaffoldService.write_file(
            module_path / "__init__.py",
            f'__version__ = "{self.config.project.version}"',
            "",
        )

        tests_path = self.root / "tests"
        ScaffoldService.ensure_dir(tests_path)
        ScaffoldService.touch(tests_path / "__init__.py")

        

    def _scaffold_app (self) -> None :
        app_path = self.get_module_path()
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
        module_path = self.get_module_path()

        ScaffoldService.ensure_dir(module_path)
        ScaffoldService.touch(module_path / "__init__.py")


    def _create_readme (self) -> None :
        ScaffoldService.from_template(self.root / "README.md", f"{str(self.category)}_README.txt")

    
    @staticmethod
    def init_package_build (root: Path) :
        config = CorelliaConfig.load(root / cs.CORELLIA_CONFIG_FILE)
        pyver = config.project.python
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
                "name": config.project.name,
                "version": config.project.version,
                "description": config.project.description,
                "readme": config.project.readme,
                "license": config.project.license,
                "keywords": config.project.keywords,
                "requires-python": f"{pyver_from},{pyver_to}",
                "authors": [
                    author.to_dict()
                    for author in config.authors
                ],
                "urls": config.urls.to_dict(),
                "dependencies": [f"{name}=={version}" for name, version in config.dependencies.items()],
                "optional-dependencies": {
                    "dev": [f"{name}=={version}" for name, version in config.dev_dependencies.items()]
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
        content = tomli_w.dumps(data)
        write_text(pyproject_path, content)



    def validate_layout (self) -> bool :
        if self.category == "package" :
            return self._validate_package()
        elif self.category == "app" :
            return self._validate_app()
        elif self.category == "deploy" :
            return self._validate_deploy()
        
        return False

    def _validate_package (self) -> bool :
        module_path = self.get_module_path()
        return(
            module_path.is_dir()
            and (module_path / "__init__.py").is_file()
        )

    def _validate_app (self) -> bool :
        module_path = self.get_module_path()
        return(
            module_path.is_dir()
            and (module_path / "__init__.py").is_file()
            and (self.root / "main.py").is_file()
        )
        
    def _validate_deploy (self) -> bool :
        module_path = self.get_module_path()
        return(
            module_path.is_dir()
            and (module_path / "__init__.py").is_file()
        )
    


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

        prefix = (
            f"{canonicalize_name(self.project_name).replace('-', '_')}"
            f"-{self.config.project.version}"
        )

        for path in dist_dir.iterdir():
            if not path.is_file():
                continue

            if path.name.startswith(prefix):
                path.unlink(missing_ok=True)