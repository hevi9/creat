import typer

from ..configs import UserConfig, x_user_config

cli = typer.Typer(name="config", no_args_is_help=True, help="Configuration commands.")


@cli.command()
def user() -> None:
    """Print the active user configuration."""
    typer.echo(x_user_config().model_dump_json(indent=2))


@cli.command()
def init(
    force: bool = typer.Option(
        False,
        help="Overwrite an existing user config file.",
    ),
) -> None:
    """Write the active user configuration to disk."""
    config_data = x_user_config()
    path = config_data.user_config_path
    if path.exists() and not force:
        typer.echo(f"Config file {path} already exists. Use --force to overwrite.")
        raise typer.Exit(1)

    path.parent.mkdir(parents=True, exist_ok=True)
    config_text = UserConfig(
        user_config_path=path,
        project_system=config_data.project_system,
    ).model_dump_json(indent=2)
    path.write_text(config_text + "\n", encoding="utf-8")
    typer.echo(f"Wrote {path}")
