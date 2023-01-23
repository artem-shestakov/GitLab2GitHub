import os
import typer
from rich.console import Console
from .utils import get, post


err_console = Console(stderr=True)
console = Console()

async def get_repo(session, name, headers) -> dict:
    resp = await get(
        session,
        f"https://api.github.com/repos/{os.environ['GH_USER']}/{name}",
        headers
        )
    if resp["code"] == 200:
        return resp["response"]
    elif resp["code"] == 404:
        return None
    else:
        err_console.print(f"⚠️ Responce code: {resp['code']}. {resp['response']['message']}")
        raise typer.Exit(1)

async def create_repo(repo_name: str, session, headers) -> dict:
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