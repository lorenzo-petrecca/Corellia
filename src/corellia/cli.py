import typer
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

app = typer.Typer(
    help="Corellia CLI",
    no_args_is_help=True
)

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



@app.callback()
def main():
    """Corellia CLI."""
    pass
