import typer
from . import mirror, states

app = typer.Typer()
app.add_typer(mirror.app, name="mirror")
