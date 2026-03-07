import typer

app = typer.Typer(help="Corellia CLI")


@app.callback()
def main():
    """Corellia main CLI."""
    pass


@app.command()
def create():
    print("create command works")