import typer
from corellia.managers import ProjectManager


def run (
    script: str = typer.Argument(
        None,
        help="Script name declared in [scripts]"
    ),
    show_list: bool = typer.Option(
        False,
        "--list",
        help="List all scripts defined in the config."
    )
) -> None:
    """
    Execute a project script declared in corellia.toml.
    """
    if script is not None and show_list :
        raise typer.BadParameter(
            "The ‘--list’ flag doesn't make sense in this context."
        )
    
    if script is None and not show_list:
        raise typer.BadParameter(
            "You must provide a script name or use '--list'."
        )
    
    project = ProjectManager()

    if show_list :
        project.list_scripts().out()
        return
    
    project.run_script(script).out()