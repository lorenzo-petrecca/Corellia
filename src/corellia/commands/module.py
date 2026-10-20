import typer

from corellia.managers import ProjectManager

app = typer.Typer(
    help="Manage the project's Python module.",
    no_args_is_help=True,
)

@app.command(
    name="rename",
    help="Rename the project's main Python module.",
)
def rename (
    name: str = typer.Argument(
        ...,
        help="New module name"
    ),
) -> None :
    """
    Rename the main module directory and update corellia.toml.
    """
    project = ProjectManager()
    project.rename_module(name).out()