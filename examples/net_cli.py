#!/usr/bin/env python3
"""A small, cron-safe network-ops CLI. Does one thing, exits with a meaningful code.

    pip install click
    python net_cli.py reachable 0.0.0.0
    python net_cli.py reachable 0.0.0.0 || echo "alert!"   # non-zero on failure
"""
import subprocess
import sys

import click


@click.group()
def cli() -> None:
    """Network ops helpers."""


@cli.command()
@click.argument("host")
@click.option("--count", "-c", default=3, show_default=True, help="probes to send")
def reachable(host: str, count: int) -> None:
    """Exit 0 if HOST answers ICMP, non-zero otherwise — cron/CI can branch on it."""
    rc = subprocess.run(
        ["ping", "-c", str(count), "-w", "5", host],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode
    click.echo(f"{host}: {'up' if rc == 0 else 'DOWN'}")
    sys.exit(rc)  # the meaningful exit code is the whole point


if __name__ == "__main__":
    cli()
