import asyncio
import typer
from . import utils


app = typer.Typer()

@app.command()
def check(repo_name: str):
    asyncio.run(utils.check_repo(repo_name))

@app.command()
def create(repo_name: str):
    asyncio.run(utils.create_repo(repo_name))
