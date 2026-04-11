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
@click.option("--angle", default=None, type=int, help="角度オフセット(30-45)")
@click.option("--count", default=None, type=int, help="繰り返し回数(2-4)")
def wave(port, angle, count):
    port = _get_port(port)
    try:
        send_command(port, wave_motion(angle=angle, count=count))
    except ValueError as e:
        raise click.ClickException(str(e))
    click.echo(f"wave送信: {port}")


@main.command()
@click.option("--port", default=None, help="シリアルポートのパス")
@click.option("--angle", default=None, type=int, help="角度オフセット(60-75)")
def love(port, angle):
    port = _get_port(port)
    try:
        send_command(port, love_motion(angle=angle))
    except ValueError as e:
        raise click.ClickException(str(e))
    click.echo(f"love送信: {port}")


@main.command()
@click.option("--port", default=None, help="シリアルポートのパス")
@click.option("--angle", default=None, type=int, help="角度オフセット(10-18)")
def sad(port, angle):
    port = _get_port(port)
    try:
        send_command(port, sad_motion(angle=angle))
    except ValueError as e:
        raise click.ClickException(str(e))
    click.echo(f"sad送信: {port}")
