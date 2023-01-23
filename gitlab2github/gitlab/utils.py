import aiohttp
import os
import typer
from rich.console import Console
from . import states
from ..github import states as gh_state
from ..github.utils import create_repo, get_auth as gh_get_auth
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
        "PRIVATE-TOKEN": f"{states['token']['value']}"
        }

async def get_project(project_id: int, session, headers):
    resp = await get(
        session,
        f"https://gitlab.com/api/v4/projects/{project_id}",
        headers=headers
    )
    if resp["code"] == 200:
        return resp['response']
    err_console.print(f"⚠️ Responce code: {resp['code']}. {resp['response']['message']}")
    raise typer.Exit(1)

async def get_mirrors(project_id: int, session) -> list:
    headers = get_auth(states)
    resp = await get(
        session,
        f"https://gitlab.com/api/v4/projects/{project_id}/remote_mirrors",
        headers=headers
        )
    if resp["code"] == 200:
        return resp['response']
    err_console.print(f"⚠️ Responce code: {resp['code']}. {resp['response']['message']}")
    raise typer.Exit(1)

async def create_push_mirror(project_id: int, url: str, session, headers=None) -> dict:
    resp = await post(
                session,
                f"https://gitlab.com/api/v4/projects/{project_id}/remote_mirrors",
                headers=headers,
                json={
                    "url": url,
                    "enabled": True
                }
            )
    if resp["code"] == 201:
        return resp['response']
    err_console.print(f"⚠️ Responce code: {resp['code']}. {resp['response']['message']}")
    raise typer.Exit(1)

async def create_mirrors(gl_project_id: int, gh_project_name: str, url=None):
    headers = get_auth(states)
    gh_headers = gh_get_auth(gh_state)
    async with aiohttp.ClientSession() as session:
        # Check GitHub repository or create it
        repository = await create_repo(gh_project_name, session=session)
        if repository:
            curret_mirrors = await get_mirrors(gl_project_id, session)
            for mirror in curret_mirrors:
                print(mirror["url"].split("@")[-1])
                if mirror["url"].split("@")[-1] == repository["html_url"].replace("https://", ""):
                    typer.echo(f"😐 Mirroring for \"{gh_project_name}\" is exists yet")
                    raise typer.Exit()
            
            # Creating mirror to GitHub
            typer.echo(f"🚧 Mirroring for \"{gh_project_name}\" is being created")
            url = f"https://{gh_state['username']['value']}:{gh_state['token']['value']}@{repository['html_url'].replace('https://','')}"
            mirror = await create_push_mirror(gl_project_id, url, session, headers=headers)
                