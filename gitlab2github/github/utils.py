import aiohttp
import os
import typer
from rich.console import Console
from rich.table import Table
from . import states


err_console = Console(stderr=True)
console = Console()

def get_auth(states: dict):
    for key, state in states.items():
        if not state["value"]:
            try:
                state["value"] = os.environ[state["env"]]
            except KeyError:
                err_console.print(f"Define {state['env']} environment or use --{key} option")
                raise typer.Exit(1)

async def get_repo(repo_name):
    make_request=True
    page = 1
    get_auth(states)
    async with aiohttp.ClientSession() as session:
        while make_request:
            async with session.get(
                f"https://api.github.com/user/repos?page={page}",
                headers={
                    "Accept": "application/vnd.github+json",
                    "Authorization": f"Bearer {states['token']['value']}",
                    "X-GitHub-Api-Version": "2022-11-28",
                    }) as resp:
                if await resp.text() == "[]":
                    make_request=False
                else:
                    page += 1
                for repo in await resp.json():
                    if repo["name"] == repo_name:
                        typer.echo(f"Repository {repo_name} is exists")
                        table = Table("ID", "Name", "Created at")
                        table.add_row(str(repo["id"]), repo["name"], repo["created_at"])
                        console.print(table)
                        raise typer.Exit()
        if not make_request:
            typer.echo(f"Repository {repo_name} is not exists")
            raise typer.Exit()
