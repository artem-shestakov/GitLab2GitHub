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

async def fetch(session, url, headers=None):
    async with session.get(url, headers=headers) as response:
        return await response.json()

async def get_repo(session, repo_name) -> dict:
    make_request=True
    page = 1
    get_auth(states)
    headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {states['token']['value']}",
        "X-GitHub-Api-Version": "2022-11-28",
        }
    while make_request:
        resp = await fetch(
            session,
            f"https://api.github.com/user/repos?page={page}",
            headers
            )
        if len(resp) == 0:
            make_request=False
        else:
            page += 1
        for repo in resp:
            if repo["name"] == repo_name:
                return {
                    "id": str(repo["id"]),
                    "name": repo["name"],
                    "created_at": repo["created_at"]
                }
    return None

async def create_repo(repo_name: str):
    async with aiohttp.ClientSession() as session:
        repo = await get_repo(session, repo_name)
        if repo:
            typer.echo(f"Repository {repo_name} is exists yet")
            raise typer.Exit()
        typer.echo(f"Creating {repo_name}")
        
        raise typer.Exit()
