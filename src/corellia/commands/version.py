import typer

from corellia.managers import ProjectManager


def version(
    target: str | None = typer.Argument(
        None,
        help="major, minor, patch or explicit version (X.Y.Z).",
    ),
) -> None:
    """
    Show or update the current project version.
    """
    project = ProjectManager()
    project.version(target).out()
