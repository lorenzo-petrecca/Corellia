import typer
from corellia.managers import ProjectManager


def sync (
    package: str | None = typer.Option(
        None,
        "--package",
        "-p",
        help="Syncronize only one declared package"
    ),
    clean: bool = typer.Option(
        False,
        "--clean",
        help="Rebuild the virtual environment from scratch before syncing."
    ),
    nodev: bool = typer.Option(
        False,
        "--no-dev",
        help="Avoid synchronizing dev-dependencies"
    )
) -> None:
    """
    Synchronize the current project environment with corellia.toml.
    """

    project = ProjectManager()

    if clean and package :
        raise typer.BadParameter (
            "You cannot use --clean and --package together."
        )
    
    if package and nodev :
        raise typer.BadParameter (
            "The --no-dev option is not compatible with the --package option."
        )
    
    if package :
        project.sync_package(package).out()
        return
    
    project.sync(clean=clean, nodev=nodev).out()