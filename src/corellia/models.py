from dataclasses import dataclass
from typing import Literal

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
        return self.framework.answer or ""
    

    def is_complete (self) -> bool :
        return (
            self.name.ok and
            self.python_version.ok and
            self.category.ok and
            self.framework.ok
        )
       

        



ScriptMode = Literal["strict", "shell"]
SCRIPT_MODES: tuple[ScriptMode, ...] = ("strict", "shell")

@dataclass
class ScriptConfig :
    name: str
    mode: ScriptMode
    command: str
    description: str | None = None