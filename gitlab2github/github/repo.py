import asyncio
import typer
from . import utils
from rich.console import Console
from rich.table import Table


app = typer.Typer()

@app.command()
def check(repo_name: str):
    asyncio.run(utils.get_repo(repo_name))