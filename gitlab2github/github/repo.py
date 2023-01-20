import os
import requests
import typer
from . import states
from rich.console import Console
from rich.table import Table

app = typer.Typer()
err_console = Console(stderr=True)
console = Console()

def get_auth(state: dict):
    for key, state in states.items():
        if not state["value"]:
            try:
                state["value"] = os.environ[state["env"]]
            except KeyError:
                err_console.print(f"Define {state['env']} environment or use --{key} option")
                raise typer.Exit(1)

@app.command()
def check(repo_name: str):
    make_request=True
    page = 1
    get_auth(states)
    while make_request:
        res = requests.get(
            f"https://api.github.com/user/repos?page={page}",
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {states['token']['value']}",
                "X-GitHub-Api-Version": "2022-11-28",
                }
            )
        if res.text == "[]":
            make_request=False
        else:
            page += 1
        for repo in res.json():
            typer.echo(repo["name"])
            if repo["name"] == repo_name:
                typer.echo(f"Repository {repo_name} is exists")
                table = Table("ID", "Name", "Created at")
                table.add_row(str(repo["id"]), repo["name"], repo["created_at"])
                console.print(table)
                raise typer.Exit()
        if not make_request:
            typer.echo(f"Repository {repo_name} is not exists")