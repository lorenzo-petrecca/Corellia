from pathlib import Path
import re
import tomllib
import tomli_w
from importlib.resources import files
from corellia.models import (
    CreateModel, 
    CorelliaConfigModel,
    ProjectSectionModel,
    EnvironmentSectionModel,
    FrameworkSectionModel,
    AuthorSectionModel,
    UrlsSectionModel,
    ScriptSectionModel, 
    ConfigIntegrityReport,
)
from corellia import constants as cs
from corellia.models import CATEGORIES, Category
from corellia.utils.file_io import write_text


def default_module_name(name: str, category: Category) -> str:
    match category:
        case "package":
            module = name.replace("-", "_")

            if module[0].isdigit():
                module = f"_{module}"

            return module

        case "app":
            return "app"

        case "deploy":
            return "config"

        case _:
            raise ValueError(f"Unsupported project category: {category}")
    


class CorelliaConfig :

    def __init__(self, model: CorelliaConfigModel, path: Path) -> None:
        self.model = model
        self.path = path

    @classmethod
    def load (cls, path: Path) -> "CorelliaConfig":
        with path.open('rb') as file :
            data = tomllib.load(file)

        model = CorelliaConfigModel.from_dict(data)
        return cls(model=model, path = path)


    @classmethod
    def from_model (
        cls, 
        path: Path, 
        create_model: CreateModel, 
        dependencies: dict[str, str]
    ) -> "CorelliaConfig" :

        django_scripts = {
            "dev": ScriptSectionModel(
                command="python manage.py runserver",
                mode="strict",
                description="Run django development server",
            ),
            "migrate": ScriptSectionModel(
                command="python manage.py migrate",
                mode="strict",
                description="Apply database migrations",
            ),
            "makemigrations": ScriptSectionModel(
                command="python manage.py makemigrations",
                mode="strict",
                description="Create new django migrations",
            ),
            "shell": ScriptSectionModel(
                command="python manage.py shell",
                mode="strict",
                description="Open django shell",
            ),
        }

        scripts_template = {
            "check": ScriptSectionModel(
                command="python --version",
                mode="strict",
                description="Check that the project Python environment works",
            ),
        }

        framework = create_model.project_framework
        if framework is not None and framework.lower().strip() == "django" :
            scripts_template.update(django_scripts)

        if create_model.project_category in CATEGORIES :
            category: Category = create_model.project_category
        else :
            category: Category = "package"


        data = CorelliaConfigModel(
            project=ProjectSectionModel(
                name=create_model.project_name,
                module=default_module_name(
                    create_model.project_name,
                    category,
                ),
                version="0.1.0",
                python=create_model.project_python_version,
                category=category,
            ),
            environment=EnvironmentSectionModel(),
            framework=FrameworkSectionModel(
                name=framework,
            ),
            dependencies=dependencies,
            scripts=scripts_template,
        )


        return cls(model=data, path=path)
    
    

    def save (self) -> None:
        content = tomli_w.dumps(self.model.to_dict())

        if not self.authors :
            template = files("corellia.templates").joinpath("authors_example.txt")
            content += "\n" + template.read_text(encoding="utf-8")

        write_text(self.path, content)
    

 
    @property
    def project (self) -> ProjectSectionModel :
        return self.model.project
    
    @property
    def environment (self) -> EnvironmentSectionModel :
        return self.model.environment
    
    @property
    def framework (self) -> FrameworkSectionModel :
        return self.model.framework
    
    @property
    def authors (self) -> list[AuthorSectionModel] :
        return self.model.authors
    
    @property
    def urls (self) -> UrlsSectionModel :
        return self.model.urls
    
    @property
    def dependencies (self) -> dict[str, str] :
        return self.model.dependencies
    
    @property
    def dev_dependencies (self) -> dict[str, str] :
        return self.model.dev_dependencies
    
    @property
    def scripts (self) -> dict[str, ScriptSectionModel] :
        return self.model.scripts
    

    
    
    def get_dependency_version (self, package: str) -> str | None :
        return self.dependencies.get(package)
    
    def get_dev_dependency_version (self, package: str) -> str | None :
        return self.dev_dependencies.get(package)
    


    def get_script (self, name: str) -> ScriptSectionModel | None :
        return self.model.scripts.get(name)
    
    

    def has_dependency (self, package: str) -> bool :
        return package in self.dependencies
    
    def has_dev_dependency (self, package: str) -> bool :
        return package in self.dev_dependencies
    

    def has_script (self, name: str) -> bool :
        return name in self.scripts
    

    def set_project_version(self, version: str) -> None:
        self.model.project.version = version
        self.save()


    def set_project_module(self, module: str) -> None:
        self.model.project.module = module
        self.save()

    
    def set_dependency (self, package: str, version: str, dev: bool) -> None:
        if dev :
            self.model.dev_dependencies[package] = version
        else :
            self.model.dependencies[package] = version

        self.save()

    def remove_dependency (self, package: str, dev: bool) -> None :
        if dev :
            self.model.dev_dependencies.pop(package, None)
        else :
            self.model.dependencies.pop(package, None)

        self.save()


    @property
    def integrity(self) -> ConfigIntegrityReport:
        return self.model.integrity

