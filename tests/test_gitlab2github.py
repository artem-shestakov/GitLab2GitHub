from gitlab2github import cli, __appname__, __version__
from typer.testing import CliRunner

runner = CliRunner()

def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert __appname__ in result.stdout
    assert __version__ in result.stdout
