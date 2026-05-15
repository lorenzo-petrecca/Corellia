from dataclasses import dataclass, field
from typing import Literal, Any, TypeAlias, Generic, TypeVar, overload
from corellia.frameworks import Framework, SUPPORTED_FRAMEWORKS
from corellia.validators import FieldValidator, Validators
import re
import copy

PromptName = Literal["name", "python_version", "category", "framework"]
Category = Literal["package", "app", "deploy"]
CATEGORIES: tuple[Category, ...] = ("package", "app", "deploy")


@dataclass
class Prompt :
    question: str 
    answer: str | None = None
    ok: bool = False

@dataclass
class CreateModel :
    name: Prompt
    python_version: Prompt
    category: Prompt
    framework: Prompt

    @classmethod
    def new (cls) -> "CreateModel" :
        return cls (
            name = Prompt("Project Name"),
            python_version=Prompt("Python version to use"),
            category=Prompt("Project category"),
            framework=Prompt("Framework"),
        )
    

    def prompt (self, prompt_name: PromptName) -> Prompt :
        return getattr(self, prompt_name)

    def with_prompt (
        self, 
        prompt_name: PromptName, 
        answer: str | None, 
        ok: bool,
    ) -> "CreateModel" :

        return CreateModel (
            name=Prompt(
                self.name.question,
                answer if prompt_name == "name" else self.name.answer,
                ok if prompt_name == "name" else self.name.ok,
            ),
            python_version=Prompt(
                self.python_version.question,
                answer if prompt_name == "python_version" else self.python_version.answer,
                ok if prompt_name == "python_version" else self.python_version.ok,
            ),
            category=Prompt(
                self.category.question,
                answer if prompt_name == "category" else self.category.answer,
                ok if prompt_name == "category" else self.category.ok,
            ),
            framework=Prompt(
                self.framework.question,
                answer if prompt_name == "framework" else self.framework.answer,
                ok if prompt_name == "framework" else self.framework.ok,
            ),
        )


    @property
    def project_name (self) -> str : 
        return self.name.answer or ""
    
    @property
    def project_python_version (self) -> str : 
        return self.python_version.answer or ""
    
    @property
    def project_category (self) -> str : 
        return self.category.answer or ""
    
    @property
    def project_framework (self) -> str : 
        return self.framework.answer or "none"
    

    def is_complete (self) -> bool :
        return (
            self.name.ok and
            self.python_version.ok and
            self.category.ok and
            self.framework.ok
        )










T = TypeVar("T")


FieldType: TypeAlias = Literal["single", "multi"]

class ConfigField(Generic[T]) :
    def __init__(
        self, 
        field_type: FieldType,
        required: bool = False,
        default: Any = None,
        validators: list[FieldValidator] | None = None,
    ) -> None:
        self._field_type: FieldType = field_type
        self._required = required
        self._default = default
        self._validators = validators or []

        self._field_name = ""
        self._storage_name = ""
        self._section_name = ""
        self._full_name = ""

    def __set_name__ (self, owner, name: str) -> None :
        self._field_name = name
        self._storage_name = f"_field_value_{name}"

        self._section_name = getattr(owner, "_section_name", owner.__name__)
        self._full_name = f"{self._section_name}.{self._field_name}"

    @overload
    def __get__ (self, instance: None, owner: type | None = None) -> "ConfigField[T]":
        ...

    @overload
    def __get__ (self, instance: object, owner: type | None = None) -> T :
        ...
        
    def __get__ (self, instance: object | None, owner: type | None = None) -> T | "ConfigField[T]" :
        if instance is None :
            return self
        
        return getattr(instance, self._storage_name, self._default)
    

    def __set__(self, instance, value: Any) -> None :
        errors = self._validate(value)

        if errors :
            instance._errors[self._full_name] = errors
        else :
            instance._errors.pop(self._full_name, None)

        setattr(instance, self._storage_name, value)

    
    def _is_empty (self, value: Any) -> bool :
        if value is None :
            return True
        
        if isinstance(value, (str, list)) :
            return len(value) == 0
        
        return False

    
    def _validate (self, value: Any) -> list[str] :
        errors: list[str] = []

        # 1. require
        errors.extend(self._validate_required(value))
        if errors :
            return errors

        # 2. type check
        errors.extend(self._validate_type(value))
        if errors :
            return errors

        # 3. extra validations
        for validator in self._validators :
            errors.extend(validator(value, self._full_name))

        return errors
    

    def _validate_required (self, value: Any) -> list[str] :
        if self._required and self._is_empty(value) :
            return [f"{self._full_name} is required"]
        return []
    
    def _validate_type(self, value: Any) -> list[str] :
        # evita che un campo opzionale con None fallisca per tipo.
        if self._is_empty(value) and not self._required :
            return []
        
        if self._field_type == "single" and not isinstance(value, str) :
            return [f"{self._full_name} must be a string"]

        if self._field_type == "multi" :
            if not isinstance(value, list) :
                return [f"{self._full_name} must be a list"]
            else :
                for el in value :
                    if not isinstance(el, str) :
                        return [f"All {self._full_name} items in the list must be strings"]       
                    
        return []
    

    @property
    def default (self) -> Any :
        return copy.deepcopy(self._default)
    
        


        

    



ConfigSectionName = Literal[
    "project",
    "environment",
    "authors",
    "urls",
    "scripts",
    "dependencies",
    "dev-dependencies",
    "framework",
]  


class ConfigSection :
    _section_name: ConfigSectionName
    
    def __init__(self, **kwargs) -> None:
        self._errors: dict[str, list[str]] = {}
        self._warnings: dict[str, list[str]] = {}

        fields = self.fields()

        # Controllo chiavi sconosciute
        unknown = set(kwargs) - set(fields)
        if unknown :
            self._warnings[self._section_name] = [
                f"Unknown field \"{name}\" ignored"
                for name in sorted(unknown)
            ]
        # ------

        for name, field in self.fields().items() :
            value = kwargs.get(name, field.default)
            setattr(self, name, value)

    @property
    def errors (self) -> dict[str, list[str]] :
        return self._errors
    
    @property
    def warnings (self) -> dict[str, list[str]] :
        return self._warnings
    
    @property
    def ok (self) -> bool :
        return len(self._errors) == 0
    

    @classmethod
    def fields (cls) -> dict[str, ConfigField] :
        return {
            name: field
            for name, field in cls.__dict__.items()
            if isinstance(field, ConfigField)
        }
    
    @classmethod
    def from_dict (cls, data: dict[str, Any]) :
        return cls(**data)

    def to_dict (self) -> dict[str, Any] :
        return {
            name: getattr(self, name)
            for name in self.fields()
        }



class ProjectSectionModel(ConfigSection) :
    _section_name: ConfigSectionName = "project"

    name: ConfigField[str] = ConfigField(
        "single", 
        required=True,
        validators=[
            Validators.regex(
                r"[a-z0-9][a-z0-9_-]*",
                "must start with a lowercase letter or number and can only contain lowercase letters, numbers, '-' and '_'",
            )
        ]
    )
    version: ConfigField[str] = ConfigField("single", required=True)
    python: ConfigField[str] = ConfigField("single", required=True)
    category: ConfigField[str] = ConfigField("single", required=True, validators=[Validators.allowed_values(set(CATEGORIES)),])
    description: ConfigField[str] = ConfigField("single", default="", validators=[Validators.max_length(250),])
    readme: ConfigField[str] = ConfigField("single", default="README.md")
    license: ConfigField[str] = ConfigField("single", default="MIT")
    keywords: ConfigField[list[str]] = ConfigField("multi", default=[])

    



Environment = Literal["pyenv"]
ENVS: tuple[Environment, ...] = ("pyenv",)

class EnvironmentSectionModel(ConfigSection) :
    _section_name: ConfigSectionName = "environment"

    manager: ConfigField[str] = ConfigField(
        "single", 
        required=True, 
        default="pyenv",
        validators=[Validators.allowed_values(set(ENVS)),]
    )
    venv: ConfigField[str] = ConfigField(
        "single",
        required=True,
        default=".venv",
    )



class FrameworkSectionModel(ConfigSection) :
    _section_name: ConfigSectionName = "framework"

    name: ConfigField[str] = ConfigField(
        "single", 
        required=True, 
        default="none", 
        validators=[Validators.allowed_values(set(SUPPORTED_FRAMEWORKS))]
    )



class UrlsSectionModel(ConfigSection) :
    _section_name: ConfigSectionName = "urls"

    site: ConfigField[str] = ConfigField("single", default="")
    repo: ConfigField[str] = ConfigField("single", default="")
    issues: ConfigField[str] = ConfigField("single", default="")

    def to_dict (self) -> dict[str, Any] :
        return {
            name: getattr(self, name)
            for name in self.fields()
            if len(getattr(self, name)) > 0
        }


class AuthorSectionModel(ConfigSection) :
    _section_name: ConfigSectionName = "authors"

    name: ConfigField[str] = ConfigField("single", required=True)
    email: ConfigField[str] = ConfigField("single", default="")





ScriptMode = Literal["strict", "shell"]
SCRIPT_MODES: tuple[ScriptMode, ...] = ("strict", "shell")


class ScriptSectionModel(ConfigSection) :
    _section_name: ConfigSectionName = "scripts"
    
    command: ConfigField[str] = ConfigField("single", required=True)
    mode: ConfigField[str] = ConfigField(
        "single",
        required=True,
        validators=[
            Validators.allowed_values(set(SCRIPT_MODES)),
        ]
    )
    description: ConfigField[str] = ConfigField("single", default="")



@dataclass
class ConfigIntegrityReport :
    errors: dict[str, list[str]] = field(default_factory=dict)
    warnings: dict[str, list[str]] = field(default_factory=dict)
    ok: bool = True

class CorelliaConfigModel :
    def __init__(
        self,
        project: ProjectSectionModel,
        environment: EnvironmentSectionModel,
        framework: FrameworkSectionModel,
        authors: list[AuthorSectionModel] | None = None,
        urls: UrlsSectionModel | None = None,
        dependencies: dict[str, str] | None = None,
        dev_dependencies: dict[str, str] | None = None,
        scripts: dict[str, ScriptSectionModel] | None = None,
    ) -> None:
        self.project = project
        self.environment = environment
        self.framework = framework
        self.authors = authors or []
        self.urls = urls or UrlsSectionModel()
        self.dependencies = dependencies or {}
        self.dev_dependencies = dev_dependencies or {}
        self.scripts = scripts or {}


    @classmethod
    def from_dict (cls, data: dict[str, Any]) -> "CorelliaConfigModel" :
        return cls(
            project=ProjectSectionModel(
                **data.get(ProjectSectionModel._section_name, {})
            ),
            environment=EnvironmentSectionModel(
                **data.get(EnvironmentSectionModel._section_name, {})
            ),
            framework=FrameworkSectionModel(
                **data.get(FrameworkSectionModel._section_name, {})
            ),
            authors=[
                AuthorSectionModel(**author)
                for author in data.get(AuthorSectionModel._section_name, [])
            ],
            urls=UrlsSectionModel(
                **data.get(UrlsSectionModel._section_name, {})
            ),
            dependencies=data.get("dependencies", {}),
            dev_dependencies=data.get("dev-dependencies", {}),
            scripts={
                name: ScriptSectionModel(**raw)
                for name, raw in data.get(ScriptSectionModel._section_name, {}).items()
            }
        )
    
    def to_dict (self) -> dict[str, Any] :
        data = {
            ProjectSectionModel._section_name: self.project.to_dict(),
            EnvironmentSectionModel._section_name: self.environment.to_dict(),
            FrameworkSectionModel._section_name: self.framework.to_dict(),
            UrlsSectionModel._section_name: self.urls.to_dict(),
            "dependencies": self.dependencies,
            "dev-dependencies": self.dev_dependencies,
            ScriptSectionModel._section_name: {
                name: script.to_dict()
                for name, script in self.scripts.items()
            },
        }

        if self.authors :
            data[AuthorSectionModel._section_name] = [
                author.to_dict()
                for author in self.authors
            ]
        
        return data


    def sections (self) -> list[ConfigSection] :
        sections: list[ConfigSection] = []
        
        for value in self.__dict__.values() :
            if isinstance(value, ConfigSection) :
                sections.append(value)

            elif isinstance(value, list) :
                sections.extend(
                    item
                    for item in value
                    if isinstance(item, ConfigSection)
                )

            elif isinstance(value, dict) :
                sections.extend(
                    item
                    for item in value.values()
                    if isinstance(item, ConfigSection)
                )
        
        return sections


    @property
    def integrity (self) -> ConfigIntegrityReport :
        # attualmente sono esclusi i controlli per le
        # sezioni "dependencies" e "dev-dependencies"
        sections = self.sections()

        errors = {}
        warnings = {}
        ok = True
        for section in sections :
            # unione di errors con ogni singola section iterata
            errors.update(section.errors)

            # unione di errors con ogni singola section iterata
            warnings.update(section.warnings)

            # aggiornamento di ok -> (rappresenta integrità, quindi solo errors)
            ok = ok and section.ok

        return ConfigIntegrityReport(
            errors=errors,
            warnings=warnings,
            ok=ok,
        )

