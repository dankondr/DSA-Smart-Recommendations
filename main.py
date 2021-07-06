#!/usr/bin/env python
import uvicorn
from typer import Typer

from core.app import app
from core.settings import settings

cli = Typer()


@cli.command()
def run() -> None:
    uvicorn.run(
        app,
        host=settings.app_host,
        port=settings.app_port,
        debug=settings.debug,
        timeout_keep_alive=settings.timeout_keep_alive,
        access_log=False,
        loop='uvloop',
        http='httptools',
        lifespan='on',
    )


@cli.command()
def useless():
    print('Hello ;)')


if __name__ == '__main__':
    cli()
