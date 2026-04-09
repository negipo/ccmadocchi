import click

from ccmadocchi.serial_comm import find_serial_port, send_command


@click.group()
def main():
    pass


def _get_port(port):
    if port is None:
        port = find_serial_port()
        if port is None:
            raise click.ClickException("デバイスが見つかりません")
    return port


@main.command()
@click.option("--port", default=None, help="シリアルポートのパス")
def wave(port):
    port = _get_port(port)
    send_command(port, "w")
    click.echo(f"wave送信: {port}")


@main.command()
@click.option("--port", default=None, help="シリアルポートのパス")
def love(port):
    port = _get_port(port)
    send_command(port, "l")
    click.echo(f"love送信: {port}")


@main.command()
@click.option("--port", default=None, help="シリアルポートのパス")
def sad(port):
    port = _get_port(port)
    send_command(port, "s")
    click.echo(f"sad送信: {port}")
