import aiohttp
import os
import typer
from rich.console import Console
from . import states
from ..utils import get, post


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
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {states['token']['value']}",
        "X-GitHub-Api-Version": "2022-11-28",
        }

async def get_repo(session, name, headers) -> dict:
    get_auth(states)
    resp = await get(
        session,
        f"https://api.github.com/repos/{states['username']['value']}/{name}",
        headers
        )
    if resp["code"] == 200:
        return resp["response"]
    elif resp["code"] == 404:
        return None
    else:
        err_console.print(f"⚠️ Responce code: {resp['code']}. {resp['response']['message']}")
        raise typer.Exit(1)

async def check_repo(name: str):
    headers = get_auth(states)
    async with aiohttp.ClientSession() as session:
        repo = await get_repo(session, name, headers)
        print(repo)
        if repo:
            typer.echo(f"😐 Repository \"{name}\" is exists yet")
            raise typer.Exit()
        typer.echo(f"😐 Repository \"{name}\" is not exists")
        raise typer.Exit()
        
async def create_repo(repo_name: str, session) -> dict:
    headers = get_auth(states)
    repository = await get_repo(session, repo_name, headers)
    if repository:
        typer.echo(f"😐 Repository \"{repo_name}\" is exists yet")
        return repository
    typer.echo(f"🚧 Repository \"{repo_name}\" is being created...")
    resp = await post(
        session,
        "https://api.github.com/user/repos",
        headers=headers,
        json={
            "name":repo_name,
            "description":"",
            "homepage":"https://github.com",
            "private": False,
            "is_template": False
        }
        )
    if resp["code"] == 201:
        typer.echo(f"🚀 Repository \"{repo_name}\" was created")
        return resp["response"]
    else:
        err_console.print(f"⚠️ Responce code: {resp['code']}. {resp['response']['message']}")
        raise typer.Exit(1)
