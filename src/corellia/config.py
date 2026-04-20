from pathlib import Path
import tomllib
import tomli_w
from typing import Any
from corellia.models import CreateModel, ScriptConfig, SCRIPT_MODES
from corellia import constants as cs


class CorelliaConfig :

    def __init__(self, data: dict[str, Any], path: Path) -> None:
        self.data = data
        self.path = path

    @classmethod
    def load (cls, path: Path) -> "CorelliaConfig":
        with path.open('rb') as file :
            data = tomllib.load(file)

        return cls(data=data, path = path)


    @classmethod
    def from_model (
        cls, 
        path: Path, 
        model: CreateModel, 
        dependencies: dict[str, str]
    ) -> "CorelliaConfig" :
        
        django_scripts_template = {
            "dev": {
                "command": "python manage.py runserver",
                "mode": "strict",
                "description": "Run django development server",
            },
            "migrate": {
                "command": "python manage.py migrate",
                "mode": "strict",
                "description": "Apply database migrations",
            },
            "makemigrations": {
                "command": "python manage.py makemigrations",
                "mode": "strict",
                "description": "Create new django migrations",
            },
            "shell": {
                "command": "python manage.py shell",
                "mode": "strict",
                "description": "Open django shell",
            },
        }

        demo_scripts_template = {
            "check": {
                "command": "python --version",
                "mode": "strict",
                "description": "Check that the project Python environment works",
            }
        }


        scripts_template = django_scripts_template if model.framework.answer == "django" else demo_scripts_template

        data = {
            cs.PROJECT_SECTION_NAME: {
                "name": model.name.answer,
                "version": "0.1.0",
                "python": model.python_version.answer,
                "category": model.category.answer,
            },
            cs.ENVIRONMENT_SECTION_NAME: {
                "manager": cs.PY_ENV_COMMAND,
                "venv": cs.DEFAULT_VENV_NAME,
            },
            cs.FRAMEWORK_SECTION_NAME: {
                "name": model.framework.answer,
            },
            cs.DEPENDENCY_SECTION_NAME: dependencies,
            cs.DEV_DEPENDENCY_SECTION_NAME: {},
            cs.SCRIPTS_SECTION_NAME: scripts_template
        }

        return cls(data=data, path=path)
    
    

    def save (self) -> None:
        with self.path.open('wb') as file :
            tomli_w.dump(self.data, file)

    def update (self, data: dict[str, Any]) :
        self.data = data

        
    def get_project_version (self) -> str :
        return self.data[cs.PROJECT_SECTION_NAME]['version']
    
    def get_project_name (self) -> str :
        return self.data[cs.PROJECT_SECTION_NAME]['name']
    
    def get_project_python_version (self) -> str :
        return self.data[cs.PROJECT_SECTION_NAME]['python']
    
    def get_project_category (self) -> str :
        return self.data[cs.PROJECT_SECTION_NAME]['category']
    
    def get_environment_manager(self) -> str:
        return self.data[cs.ENVIRONMENT_SECTION_NAME]["manager"]
    
    def get_framework_name (self) -> str :
        return self.data[cs.FRAMEWORK_SECTION_NAME]['name']
    
    def get_dependencies (self) -> dict[str, str] :
        return self.data.get(cs.DEPENDENCY_SECTION_NAME, {})
    
    def get_dev_dependencies (self) -> dict[str, str] :
        return self.data.get(cs.DEV_DEPENDENCY_SECTION_NAME, {})
    
    def get_dependency_version (self, package: str) -> str | None :
        return self.get_dependencies().get(package)
    
    def get_dev_dependency_version (self, package: str) -> str | None :
        return self.get_dev_dependencies().get(package)
    
    def get_virtual_env_name (self) -> str :
        return self.data[cs.ENVIRONMENT_SECTION_NAME]['venv']
    
    def get_scripts(self) -> dict[str, dict[str, Any]] :
        return self.data.get(cs.SCRIPTS_SECTION_NAME, {})
    
    def get_script (self, name: str) -> ScriptConfig | None :
        raw = self.get_scripts().get(name, None)
        if raw is None :
            return None
        
        if not isinstance(raw, dict) :
            raise ValueError (
                f"Script '{name}' must be declared as a table in [{cs.SCRIPTS_SECTION_NAME}.{name}]"
            )
        
        command = raw.get('command')
        mode = raw.get('mode')
        description = raw.get('description')

        if not isinstance(command, str) or not command.strip() :
            raise ValueError(
                f"Script '{name}' must define a non-empty command."
            )
        
        if mode not in SCRIPT_MODES :
            raise ValueError (
                f"Script '{name}' must define a valid mode"
            )
        
        if description is not None and not isinstance(description, str) : 
            raise ValueError(
                f"Script '{name}' has an invalid 'description'. It must be a string."
            )

        return ScriptConfig (
            name=name,
            mode=mode,
            command=command,
            description=description,
        )
    
    def get_script_list (self) -> list[ScriptConfig] : 
        """Ottiene script già validati e in forma di lista per poter essere usati facilmente"""
        scripts: list[ScriptConfig] = []

        for name in self.get_scripts() :
            script = self.get_script(name)
            if script is not None :
                scripts.append(script)

        return scripts

    


    def has_dependency (self, package: str) -> bool :
        return package in self.get_dependencies()
    
    def has_dev_dependency (self, package: str) -> bool :
        return package in self.get_dev_dependencies()
    

    def has_script (self, name: str) -> bool :
        return name in self.get_scripts()
    


    
    def set_dependency (self, package: str, version: str, dev: bool) -> None:
        key = cs.DEV_DEPENDENCY_SECTION_NAME if dev else cs.DEPENDENCY_SECTION_NAME
        deps = dict(self.data.get(key, {}))
        deps[package] = version
        self.data[key] = deps
        self.save()

    def remove_dependency (self, package: str, dev: bool) -> None :
        key = cs.DEV_DEPENDENCY_SECTION_NAME if dev else cs.DEPENDENCY_SECTION_NAME
        deps = dict(self.data.get(key, {}))
        deps.pop(package, None)
        self.data[key] = deps
        self.save()
