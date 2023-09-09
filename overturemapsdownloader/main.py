import typer


app = typer.Typer()


@app.callback()
def callback():
    """
    Awesome OMDownloader
    """


@app.command()
def shoot():
    """
    Shoot the OMDownloader
    """
    typer.echo("Shooting OMDownloader")


@app.command()
def load():
    """
    Load the OMDownloader
    """
    typer.echo("Loading OMDownloader")
