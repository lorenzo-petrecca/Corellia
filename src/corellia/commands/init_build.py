import typer
from corellia.managers import ProjectManager


def init_build () -> None:
    """
    Initialize build files for the current Corellia project.
    """

    project = ProjectManager()
    project.init_build().out()