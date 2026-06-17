"""Tests for net_cli — the boring 20% that makes a tool safe to run unattended.

Click's CliRunner invokes the command in-process and captures the exit code, so we can
assert on behavior without shelling out.

    pip install click pytest
    pytest
"""
from click.testing import CliRunner

from net_cli import cli


def test_reachable_loopback_exits_zero():
    # loopback always answers; the command must report 'up' and exit 0
    result = CliRunner().invoke(cli, ["reachable", "127.0.0.1", "-c", "1"])
    assert result.exit_code == 0
    assert "up" in result.output


def test_reachable_bad_host_exits_nonzero():
    # an unroutable address must fail closed (non-zero) so cron/CI alerts
    result = CliRunner().invoke(cli, ["reachable", "0.0.0.0", "-c", "1"])
    assert result.exit_code != 0
