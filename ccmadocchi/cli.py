import click

from ccmadocchi.serial_comm import find_serial_port, send_command


@click.group()
def main():
    pass


@main.command()
@click.option("--port", default=None, help="シリアルポートのパス")
def wave(port):
    if port is None:
        port = find_serial_port()
        if port is None:
            raise click.ClickException("デバイスが見つかりません")
    send_command(port, "w")
    click.echo(f"wave送信: {port}")
