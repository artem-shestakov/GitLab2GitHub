import typer

from .github.cli import app as github_app
from gitlab2github import __appname__, __version__


app = typer.Typer()
app.add_typer(github_app, name="github")

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__appname__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        help="Show program's version number",
        callback=_version_callback,
        is_eager=True
    )
) -> None:
    return
