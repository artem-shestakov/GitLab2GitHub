import typer

from gitlab2github import __appname__, __version__
from .github.cli import app as github_app
from .gitlab.cli import app as gitlab_app

app = typer.Typer()
app.add_typer(github_app, name="github")
app.add_typer(gitlab_app, name="gitlab")

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
