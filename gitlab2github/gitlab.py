import aiohttp
import os
import typer
from gitlab2github import __env__
from rich.console import Console
from .utils import get, post
from .github import create_repo


# stderr and stdout console
err_console = Console(stderr=True)
console = Console()

async def get_project(project_id: int, session, headers):
    """Get GitLab project information by id"""
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
    """Get list of mirrors of GitLab project"""
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
    """Create push mirror for GitLab project"""
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

async def mirror_repository(gl_project_id: int, gh_project_name: str, url=None):
    """
    Create GitHub repository and mirroring GitLab repository and
    created GitHub repository
    """
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

        # Check current mirrors
        if repository:
            curret_mirrors = await get_mirrors(gl_project_id, session, headers=gl_headers)
            for mirror in curret_mirrors:
                if mirror["url"].split("@")[-1] == repository["html_url"].replace("https://", ""):
                    typer.echo(f"😐 Mirror for \"{gh_project_name}\" is exists yet")
                    raise typer.Exit()

            # Creating mirror to GitHub
            typer.echo(f"🪞  Mirror for \"{gh_project_name}\" is being created...")
            url = f"https://{os.environ['GH_USER']}:{os.environ['GH_TOKEN']}@{repository['html_url'].replace('https://','')}"
            mirror = await create_push_mirror(gl_project_id, url, session, headers=gl_headers)
            if mirror:
                typer.echo(f"👍 Mirror for \"{gh_project_name}\" was created")
                