import click

from ccmadocchi.motions import love as love_motion
from ccmadocchi.motions import sad as sad_motion
from ccmadocchi.motions import wave as wave_motion
from ccmadocchi.motions import yo as yo_motion
from ccmadocchi.serial_comm import find_serial_port, send_command


@click.group()
def main():
    pass


def _get_port(port: str | None) -> str | None:
    if port is None:
        port = find_serial_port()
    return port


def _run_motion(port: str | None, command: str, name: str, *, silent: bool, debug: bool = False) -> None:
    port = _get_port(port)
    if port is None:
        if not silent:
            click.echo("デバイスが見つかりません")
        return
    send_command(port, command, debug=debug)
    if not silent:
        click.echo(f"{name}送信: {port}")


@main.command()
@click.option("--port", default=None, help="シリアルポートのパス")
@click.option("--silent", is_flag=True, help="出力を抑制する")
@click.option("--debug", is_flag=True, help="デバッグモード(ブザーで通知)")
@click.option("--angle", default=None, type=int, help="角度オフセット(30-45)")
@click.option("--hold", default=None, type=int, help="保持時間ms(100-300)")
def yo(port, silent, debug, angle, hold):
    try:
        _run_motion(port, yo_motion(angle=angle, hold=hold), "yo", silent=silent, debug=debug)
    except ValueError as e:
        raise click.ClickException(str(e))


@main.command()
@click.option("--port", default=None, help="シリアルポートのパス")
@click.option("--silent", is_flag=True, help="出力を抑制する")
@click.option("--debug", is_flag=True, help="デバッグモード(ブザーで通知)")
@click.option("--angle", default=None, type=int, help="角度オフセット(30-45)")
@click.option("--count", default=None, type=int, help="繰り返し回数(2-4)")
@click.option("--hold", default=None, type=int, help="保持時間ms(100-300)")
def wave(port, silent, debug, angle, count, hold):
    try:
        _run_motion(port, wave_motion(angle=angle, count=count, hold=hold), "wave", silent=silent, debug=debug)
    except ValueError as e:
        raise click.ClickException(str(e))


@main.command()
@click.option("--port", default=None, help="シリアルポートのパス")
@click.option("--silent", is_flag=True, help="出力を抑制する")
@click.option("--debug", is_flag=True, help="デバッグモード(ブザーで通知)")
@click.option("--angle", default=None, type=int, help="角度オフセット(60-75)")
@click.option("--hold", default=None, type=int, help="保持時間ms(600-900)")
def love(port, silent, debug, angle, hold):
    try:
        _run_motion(port, love_motion(angle=angle, hold=hold), "love", silent=silent, debug=debug)
    except ValueError as e:
        raise click.ClickException(str(e))


@main.command()
@click.option("--port", default=None, help="シリアルポートのパス")
@click.option("--silent", is_flag=True, help="出力を抑制する")
@click.option("--debug", is_flag=True, help="デバッグモード(ブザーで通知)")
@click.option("--angle", default=None, type=int, help="角度オフセット(10-18)")
@click.option("--hold", default=None, type=int, help="保持時間ms(1500-2500)")
def sad(port, silent, debug, angle, hold):
    try:
        _run_motion(port, sad_motion(angle=angle, hold=hold), "sad", silent=silent, debug=debug)
    except ValueError as e:
        raise click.ClickException(str(e))
