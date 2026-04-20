import typer
from corellia.managers import ProjectManager


def add (
    package: str = typer.Argument(..., help="Package name from PyPI"),
    version: str | None = typer.Option(
        None,
        "--version",
        "-v",
        help="Specific version to install."
    ),
    dev: bool = typer.Option(
        False,
        "--dev",
        help="Add the package to [dev-dependencies] instead of [dependencies]."
    )
) -> None:
    """
    Add or update a dependency in corellia.toml and install it.
    """

    project = ProjectManager()
    project.add_package(
        package=package,
        version=version,
        dev=dev
    ).out()