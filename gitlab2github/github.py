import os
import typer
from rich.console import Console
from .utils import get, post, make_request, encrypt


err_console = Console(stderr=True)
console = Console()

def check_response(response):
    """Check response code and return value from response"""
    if response["code"] == 200:
        return response["response"]
    elif response["code"] == 404:
        return None
    else:
        err_console.print(f"⚠️ Responce code: {response['code']}. {response['response']['message']}")
        raise typer.Exit(1)

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

async def get_public_key(session, repo_name, headers) -> dict:
    resp = await make_request(
        "GET",
        session,
        f"https://api.github.com/repos/{os.environ['GH_USER']}/{repo_name}/actions/secrets/public-key",
        headers=headers
    )
    return check_response(resp)


async def get_secret(session, repository: str, secret_name: str, headers):
    """Get GitHub repository secret"""
    resp = await get(
        session,
        f"https://api.github.com/repos/{os.environ['GH_USER']}/{repository}/actions/secrets/{secret_name}",
        headers=headers
        )
    return check_response(resp)

async def create_secret(session, repo_name: str, secret_name: str, value: str, headers) -> dict:
    """Create new GutHub repository secret or update if it exists"""
    secret = await get_secret(session, repo_name, secret_name, headers)
    if secret:
        typer.echo(f"🤫 Secret \"{secret_name}\" will be updated")
    else:
        typer.echo(f"🤫 Secret \"{secret_name}\" will be created")
    public_key = await get_public_key(session, repo_name, headers)
    encrypted_value = encrypt(public_key["key"], value)
    resp = await make_request(
        "put",
        session,
        f"https://api.github.com/repos/{os.environ['GH_USER']}/{repo_name}/actions/secrets/{secret_name}",
        headers=headers,
        json={
            "encrypted_value": encrypted_value,
            "key_id": public_key["key_id"]
        }
    )
    if resp["code"] == 201:
        typer.echo(f"🤐 Secret \"{secret_name}\" was created")
        return resp["response"]
    if resp["code"] == 204:
        typer.echo(f"🤐 Secret \"{secret_name}\" was updated")
        return secret
    else:
        err_console.print(f"⚠️ Responce code: {resp['code']}. {resp['response']['message']}")
        raise typer.Exit(1)


