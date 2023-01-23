import asyncio
import typer
from . import utils


app = typer.Typer()

@app.command()
def create(
    id: int = typer.Argument(None, help="GitLab project ID"),
    project: str = typer.Argument(None, help="GitHub project name")
    ):
    """
    Create a push mirror from Gitlab project to GitHub project.
    """
    asyncio.run(utils.create_mirrors(id, project.lower()))