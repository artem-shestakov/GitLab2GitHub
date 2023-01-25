import asyncio
import os
import typer
from gitlab2github import __appname__, __version__, __env__
from rich.console import Console
from .gitlab import mirror_repository


app = typer.Typer()
err_console = Console(stderr=True)
console = Console()

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

@app.command()
def mirror(
    id: int = typer.Argument(
        None, 
        help="GitLab project ID",
        metavar="GL_PROJECT_ID"),
    name: str = typer.Argument(
        None, 
        help="GitHub project name",
        metavar="GH_PROJECT_NAME"),
    secrets: str = typer.Option(
        "", 
        "--secrets",
        "-s",
        help="Create/update GitHub repository secrets as key=value. Multiple secrets separated by a comma"
        )
    ):
    """
    Create a push mirror from Gitlab project to GitHub project.
    """
    for env in __env__:
        try:
            os.environ[env]
        except KeyError:
            err_console.print(f"Variable \"{env}\" is not defined")
            raise typer.Exit(1)
    asyncio.run(mirror_repository(id, name.lower(), secrets))