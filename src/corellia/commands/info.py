import typer
from corellia.managers import ProjectManager


def info () -> None:
    """
    Shows corellia project info
    """

    project = ProjectManager()
    project.info().out()