import typer
from . import repo
from . import states

app = typer.Typer()
app.add_typer(repo.app, name="repo")


@app.callback()
def main(
    username: str = typer.Option(
        None,
        "--user",
        "-u",
        help="Github username. Default GH_USER variable",
        is_eager=True
    ),
    token: str = typer.Option(
        None,
        "--token",
        "-t",
        help="GitHub access token",
        is_eager=True
    )
) -> None:
    states["username"]["value"] = username
    states["token"]["value"] = token