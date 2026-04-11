# ccmadocchi

USB経由でぬいぐるみの腕をサーボモーターで動かすCLIツール。

## 変更時のワークフロー

### Pythonコードのみ変更した場合

```bash
uv run pytest -v
uv tool install --force --reinstall ccmadocchi --from .
```

テスト実行後、CLIを再インストールする。`--reinstall`を忘れるとキャッシュから古いコードがインストールされる。

### Arduinoコード(ino)を変更した場合

REST_ANGLEを変更する場合は、書き込み前にユーザにアームを外すよう指示すること。書き込み直後にサーボがREST_ANGLEの位置に移動するため、アームが付いたままだと破損の恐れがある。

```bash
arduino-cli compile --fqbn arduino:avr:nano arduino/ccmadocchi
arduino-cli upload --fqbn arduino:avr:nano --port /dev/cu.usbmodem201912341 arduino/ccmadocchi
```

ポートは`arduino-cli board list`で確認する。Maker NanoはArduino Nano互換(`arduino:avr:nano`)。

### 両方変更した場合

上記の両方を実行する。

## テスト

```bash
uv run pytest -v
```
