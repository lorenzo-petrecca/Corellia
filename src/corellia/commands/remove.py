import typer
from corellia.managers import ProjectManager


def remove (
    package: str = typer.Argument(..., help="Package name to remove"),
) -> None:
    """
    Remove a dependency from corellia.toml and uninstall it.
    """

    project = ProjectManager()
    project.remove_package(package).out()