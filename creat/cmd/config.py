import typer

from ..configs import Config, x_config

cli = typer.Typer(name="config", no_args_is_help=True, help="Configuration commands.")


@cli.command()
def show() -> None:
    """Print the active configuration."""
    typer.echo(x_config().model_dump_json(indent=2))


@cli.command()
def init(
    force: bool = typer.Option(
        False,
        help="Overwrite an existing config file.",
    ),
) -> None:
    """Write the active configuration to disk."""
    config_data = x_config()
    path = config_data.config_path
    if path.exists() and not force:
        typer.echo(f"Config file {path} already exists. Use --force to overwrite.")
        raise typer.Exit(1)

    path.parent.mkdir(parents=True, exist_ok=True)
    config_text = Config(
        config_path=path,
        project_system=config_data.project_system,
    ).model_dump_json(indent=2)
    path.write_text(config_text + "\n", encoding="utf-8")
    typer.echo(f"Wrote {path}")
