import typer
import importlib.metadata
from corellia.commands import (
    create,
    sync,
    add,
    remove,
    run,
    info,
    init_build,
    build,
)


PACKAGE_NAME = "corellia-cli"



def version_cb (value: bool) -> None :
    if not value :
        return
    
    try :
        cli_version = importlib.metadata.version(PACKAGE_NAME)
    except importlib.metadata.PackageNotFoundError:
        cli_version = "unknown"

    typer.echo(f"{cli_version}")
    raise typer.Exit()




app = typer.Typer(
    help="Corellia CLI",
    no_args_is_help=True
)


@app.callback()
def main(
    show_version: bool = typer.Option(
        False,
        "--version",
        "-v",
        callback=version_cb,
        is_eager=True,
        help="Show Corellia CLI version",
    )
) -> None :
    pass




app.command(
    name="create",
    help="Create a new Corellia project."
)(create)

app.command(
    name="sync",
    help="Synchronize the project environment."
)(sync)

app.command(
    name="add",
    help="Add a dependency to the project."
)(add)

app.command(
    name="remove",
    help="Remove a dependency from the project."
)(remove)

app.command(
    name="run",
    help="Run a script declared in the project."
)(run)

app.command(
    name="info",
    help="Show Corellia project info"
)(info)

app.command(
    name="init-build",
    help="Initialize build files for the current Corellia project."
)(init_build)

app.command(
    name="build",
    help="Build the current Corellia package project."
)(build)

