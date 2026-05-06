import typer
from corellia.managers import ProjectManager


def init_build (
    force: bool = typer.Option(
        False,
        "--force",
        help="Regenerate existing build files"
    )
) -> None:
    """
    Initialize build files for the current Corellia project.
    """

    project = ProjectManager()
    project.init_build(force).out()