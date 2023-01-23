import aiohttp
import os
import typer
from gitlab2github import __env__
from rich.console import Console
from .utils import get, post
from .github import create_repo


err_console = Console(stderr=True)
console = Console()
states = {}

def get_auth(states: dict):
    for env in __env__:
        try:
            states[env] = os.environ[env]
        except KeyError:
            err_console.print(f"Variable \"{env}\" is not defined")
            raise typer.Exit(1)
    return ({
        "PRIVATE-TOKEN": f"{states['GL_TOKEN']}"
        },
        {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {states['GH_TOKEN']}",
        "X-GitHub-Api-Version": "2022-11-28",
        })

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

async def get_mirrors(project_id: int, session, headers) -> list:
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
    gl_headers = {
        "PRIVATE-TOKEN": f"{os.environ['GL_TOKEN']}"
        }
    gh_headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {os.environ['GH_TOKEN']}",
        "X-GitHub-Api-Version": "2022-11-28",
        }
    async with aiohttp.ClientSession() as session:
        # Check GitHub repository or create it
        repository = await create_repo(gh_project_name, session=session, headers=gh_headers)
        if repository:
            curret_mirrors = await get_mirrors(gl_project_id, session, headers=gl_headers)
            for mirror in curret_mirrors:
                if mirror["url"].split("@")[-1] == repository["html_url"].replace("https://", ""):
                    typer.echo(f"😐 Mirroring for \"{gh_project_name}\" is exists yet")
                    raise typer.Exit()

            # Creating mirror to GitHub
            typer.echo(f"🚧 Mirroring for \"{gh_project_name}\" is being created")
            url = f"https://{os.environ['GH_USER']}:{os.environ['GH_TOKEN']}@{repository['html_url'].replace('https://','')}"
            mirror = await create_push_mirror(gl_project_id, url, session, headers=gl_headers)
                