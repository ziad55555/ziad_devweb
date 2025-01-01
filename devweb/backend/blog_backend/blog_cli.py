import typer
import uvicorn

blog_cli = typer.Typer()

@blog_cli.command()
def start_server(
    host: str = "localhost",
    port: int = 9456,
    root_path: str = "",
    workers: int = 1
):
    uvicorn.run(
        "blog_backend.blog_api:app",
        host=host,
        port=port,
        root_path=root_path,
        workers=workers,
        reload=True,
    )


