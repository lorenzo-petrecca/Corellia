import typer
from corellia.managers import ProjectManager


def build () -> None:
    """
    Build the current Corellia package project.
    """
    project = ProjectManager()
    project.build().out()