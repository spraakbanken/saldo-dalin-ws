import os
from typing import Optional

import dotenv
import typer
from sblex.socket_lookup.core import SocketLookupService

__version__ = "0.1.0"
app = typer.Typer(help="SALDO/DALIN-WS CLI")


def version_callback(value: bool) -> None: # noqa: FBT001
    if value:
        print(f"SALDO/DALIN-WS CLI {__version__}")
        raise typer.Exit()

@app.callback()
def load_dotenv(version: Optional[bool] = typer.Option(None, callback=version_callback, is_eager=True)): # noqa: B008
    print("loading dotenv ...")
    dotenv.load_dotenv(".env")



@app.command()
def lookup_lemma(lemma: str) -> None:
    """Lookup a lemma through FM.

    Parameters
    ----------
    lemma : str
        lemma to lookup
    """
    lookup_service = SocketLookupService(sem_port=int(os.environ["SALDO_SEM_PORT"]))
    print(lookup_service.lookup_lemma(lemma=lemma))

