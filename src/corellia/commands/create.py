import typer
from corellia.models import CreateModel, PromptName
from corellia.managers import ProjectManager
from typing import Callable




#   ----------------------------------
#       Model Check Callbacks
#   ----------------------------------

def name_check_callback (project: ProjectManager, value: str | None) -> bool :
    if not value:
        return False
    
    res = project.assign_name(value)
    if not res.ok :
        res.out()
        return False
    
    return True


def py_version_check_callback (project: ProjectManager, value: str | None) -> bool :
    if not value :
        return False
    
    res = project.check_py_version(value)
    if not res.ok :
        res.out()
        return False
    
    return True


def framework_check_callback (project: ProjectManager, value: str | None) -> bool :
    if not value:
        return False
    
    res = project.check_framework(value)
    if not res.ok :
        res.out()
        return False
    return True


def category_check_callback (project: ProjectManager, value: str | None) -> bool :
    if not value :
        return False
    
    res = project.check_category(value)
    if not res.ok :
        res.out()
        return False
    
    return True



def non_empty_check (project: ProjectManager, value: str | None) -> bool :
    return bool(value)


#   -----------------------------------------------------------










def collect_prompt (
    project: ProjectManager,
    model: CreateModel,
    prompt_name: PromptName,
    check: Callable[[ProjectManager, str | None], bool],
    initial_value: str | None = None,
    permissive: bool = False,
) -> CreateModel :
    value = initial_value

    while not model.prompt(prompt_name).ok :
        if not value :
            value = typer.prompt(model.prompt(prompt_name).question)

        if permissive and value is not None and isinstance(value, str) :
            value = value.strip().lower()

        is_ok = check(project, value)
        model = model.with_prompt(prompt_name, value, is_ok)

        if not is_ok :
            value = None

    return model



#   ----------------------------------
#       Project Create Command (CLI)
#   ----------------------------------

def create (
    name: str = typer.Argument(None, help="Project name")
) -> None :
    """
    Create a new Corellia project.
    """

    project_manager = ProjectManager()
    model = CreateModel.new() # creazione modello dei prompt

    # colleziona nome del progetto
    model = collect_prompt(
        project=project_manager,
        model=model,
        prompt_name="name",
        check=name_check_callback,
        initial_value=name
    )

    # verifica dell'esistenza del python manager (pyenv)
    project_manager.check_py_manager().out()

    # stampa a schermo la lista delle versioni python disponibili (o errore)
    project_manager.get_py_versions_list().out()

    # collezione versione python del progetto
    model = collect_prompt(
        project=project_manager,
        model=model,
        prompt_name="python_version",
        check=py_version_check_callback,
    )

    # stampa a schermo la lista delle categorie supportate
    project_manager.get_supported_categories().out()

    # collezione category (tipologia di progetto)
    model = collect_prompt(
        project=project_manager,
        model=model,
        prompt_name="category",
        check=category_check_callback,
        permissive=True,
    )

    # stampa a schermo la lista dei framework supportati
    project_manager.get_supported_frameworks().out()

    # collezione framework
    model = collect_prompt(
        project=project_manager,
        model=model,
        prompt_name="framework",
        check=framework_check_callback,
        permissive=True,
    )

    


    
    project_manager.bootstrap(model).out()

