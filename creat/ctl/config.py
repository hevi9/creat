import typer

from creat.configs import format_config, get_config, write_config

cli = typer.Typer(name="config", no_args_is_help=True, help="Configuration commands.")


@cli.command()
def show() -> None:
    """Print the active configuration."""
    typer.echo(format_config(get_config()), nl=False)


@cli.command()
def init(
    force: bool = typer.Option(
        False,
        help="Overwrite an existing config file.",
    ),
) -> None:
    """Write the active configuration to disk."""
    config_data = get_config()
    path = config_data.config_path
    if path.exists() and not force:
        typer.echo(f"Config file {path} already exists. Use --force to overwrite.")
        raise typer.Exit(1)

    write_config(config_data)
    typer.echo(f"Wrote {path}")
