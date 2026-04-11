import click

from ccmadocchi.motions import love as love_motion
from ccmadocchi.motions import sad as sad_motion
from ccmadocchi.motions import wave as wave_motion
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
    send_command(port, wave_motion())
    click.echo(f"wave送信: {port}")


@main.command()
@click.option("--port", default=None, help="シリアルポートのパス")
def love(port):
    port = _get_port(port)
    send_command(port, love_motion())
    click.echo(f"love送信: {port}")


@main.command()
@click.option("--port", default=None, help="シリアルポートのパス")
def sad(port):
    port = _get_port(port)
    send_command(port, sad_motion())
    click.echo(f"sad送信: {port}")
