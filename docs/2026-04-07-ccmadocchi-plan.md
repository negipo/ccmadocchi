# ccmadocchi Implementation Plan

> For agentic workers: REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

Goal: USB経由でMaker Nanoに信号を送り、SG90サーボでぬいぐるみの腕を動かすCLIツールを作る

Architecture: Python CLIがpyserial経由でMaker Nanoにコマンドを送信し、Maker Nano上のArduinoスケッチがServoライブラリでSG90を制御する。CLIは`uv tool install .`でインストールする単独コマンド。

Tech Stack: Python 3.11+, pyserial, click, uv, Arduino IDE, Servo.h

---

## File Structure

```
ccmadocchi/
├── .gitignore
├── LICENSE
├── pyproject.toml           # パッケージ定義・CLIエントリポイント・依存関係
├── ccmadocchi/
│   ├── __init__.py          # バージョン定義
│   ├── cli.py               # clickベースのCLIエントリポイント
│   └── serial_comm.py       # シリアル通信の送受信
├── arduino/
│   └── ccmadocchi/
│       └── ccmadocchi.ino   # Arduinoスケッチ（サーボ制御）
└── tests/
    ├── __init__.py
    ├── test_cli.py           # CLIのテスト
    └── test_serial_comm.py   # シリアル通信のテスト
```

---

### Task 1: プロジェクトの骨格を作る

Files:
- Create: `pyproject.toml`
- Create: `ccmadocchi/__init__.py`
- Create: `tests/__init__.py`

- [ ] Step 1: pyproject.tomlを作成

```toml
[project]
name = "ccmadocchi"
version = "0.1.0"
description = "USB経由でぬいぐるみの腕をサーボモーターで動かすCLIツール"
requires-python = ">=3.11"
dependencies = [
    "click>=8.0",
    "pyserial>=3.5",
]

[project.scripts]
ccmadocchi = "ccmadocchi.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[dependency-groups]
dev = [
    "pytest>=8.0",
]
```

- [ ] Step 2: `ccmadocchi/__init__.py`を作成

```python
__version__ = "0.1.0"
```

- [ ] Step 3: `tests/__init__.py`を作成（空ファイル）

- [ ] Step 4: 依存関係をインストールして確認

Run: `cd /Users/negipo/src/github.com/negipo/ccmadocchi && uv sync`
Expected: 依存関係がインストールされる

- [ ] Step 5: コミット

```bash
git add pyproject.toml ccmadocchi/__init__.py tests/__init__.py uv.lock .python-version
```

---

### Task 2: シリアル通信モジュールを作る

Files:
- Create: `ccmadocchi/serial_comm.py`
- Create: `tests/test_serial_comm.py`

- [ ] Step 1: テストを書く

```python
from unittest.mock import MagicMock, patch

from ccmadocchi.serial_comm import send_command, find_serial_port


class TestSendCommand:
    @patch("ccmadocchi.serial_comm.serial.Serial")
    def test_send_wave_command(self, mock_serial_class):
        mock_serial = MagicMock()
        mock_serial_class.return_value.__enter__ = MagicMock(return_value=mock_serial)
        mock_serial_class.return_value.__exit__ = MagicMock(return_value=False)

        send_command("/dev/ttyUSB0", "w")

        mock_serial_class.assert_called_once_with("/dev/ttyUSB0", 9600, timeout=2)
        mock_serial.write.assert_called_once_with(b"w")


class TestFindSerialPort:
    @patch("ccmadocchi.serial_comm.serial.tools.list_ports.comports")
    def test_find_port_returns_first_match(self, mock_comports):
        mock_port = MagicMock()
        mock_port.device = "/dev/cu.usbmodem1234"
        mock_port.description = "Maker Nano"
        mock_comports.return_value = [mock_port]

        result = find_serial_port()

        assert result == "/dev/cu.usbmodem1234"

    @patch("ccmadocchi.serial_comm.serial.tools.list_ports.comports")
    def test_find_port_returns_none_when_empty(self, mock_comports):
        mock_comports.return_value = []

        result = find_serial_port()

        assert result is None
```

- [ ] Step 2: テストが失敗することを確認

Run: `uv run pytest tests/test_serial_comm.py -v`
Expected: ImportError

- [ ] Step 3: `serial_comm.py`を実装

```python
import serial
import serial.tools.list_ports


def find_serial_port() -> str | None:
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "usbmodem" in port.device or "usbserial" in port.device:
            return port.device
    return None


def send_command(port: str, command: str) -> None:
    with serial.Serial(port, 9600, timeout=2) as ser:
        ser.write(command.encode())
```

- [ ] Step 4: テストが通ることを確認

Run: `uv run pytest tests/test_serial_comm.py -v`
Expected: 3 passed

- [ ] Step 5: コミット

```bash
git add ccmadocchi/serial_comm.py tests/test_serial_comm.py
```

---

### Task 3: CLIを作る

Files:
- Create: `ccmadocchi/cli.py`
- Create: `tests/test_cli.py`

- [ ] Step 1: テストを書く

```python
from unittest.mock import patch

from click.testing import CliRunner

from ccmadocchi.cli import main


class TestWaveCommand:
    @patch("ccmadocchi.cli.send_command")
    @patch("ccmadocchi.cli.find_serial_port", return_value="/dev/cu.usbmodem1234")
    def test_wave_sends_command(self, mock_find, mock_send):
        runner = CliRunner()
        result = runner.invoke(main, ["wave"])

        assert result.exit_code == 0
        mock_send.assert_called_once_with("/dev/cu.usbmodem1234", "w")

    @patch("ccmadocchi.cli.find_serial_port", return_value=None)
    def test_wave_fails_when_no_device(self, mock_find):
        runner = CliRunner()
        result = runner.invoke(main, ["wave"])

        assert result.exit_code != 0
        assert "見つかりません" in result.output

    @patch("ccmadocchi.cli.send_command")
    def test_wave_with_explicit_port(self, mock_send):
        runner = CliRunner()
        result = runner.invoke(main, ["wave", "--port", "/dev/ttyUSB0"])

        assert result.exit_code == 0
        mock_send.assert_called_once_with("/dev/ttyUSB0", "w")
```

- [ ] Step 2: テストが失敗することを確認

Run: `uv run pytest tests/test_cli.py -v`
Expected: ImportError

- [ ] Step 3: `cli.py`を実装

```python
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
```

- [ ] Step 4: テストが通ることを確認

Run: `uv run pytest tests/test_cli.py -v`
Expected: 3 passed

- [ ] Step 5: 全テスト通ることを確認

Run: `uv run pytest -v`
Expected: 6 passed

- [ ] Step 6: コミット

```bash
git add ccmadocchi/cli.py tests/test_cli.py
```

---

### Task 4: CLIをインストールして動作確認

Files:
- なし（インストールと確認のみ）

- [ ] Step 1: `uv tool install`でインストール

Run: `uv tool install --force /Users/negipo/src/github.com/negipo/ccmadocchi`
Expected: `ccmadocchi`が`~/.local/bin`にインストールされる

- [ ] Step 2: CLIが動くことを確認

Run: `ccmadocchi --help`
Expected: ヘルプが表示される（waveサブコマンドが見える）

- [ ] Step 3: デバイス未接続時のエラーを確認

Run: `ccmadocchi wave`
Expected: 「デバイスが見つかりません」エラー

- [ ] Step 4: コミット不要（コード変更なし）

---

### Task 5: Arduinoスケッチを作る

Files:
- Create: `arduino/ccmadocchi/ccmadocchi.ino`

- [ ] Step 1: Arduinoスケッチを作成

```cpp
#include <Servo.h>

Servo servo;
const int SERVO_PIN = 9;
const int REST_ANGLE = 45;

void setup() {
    servo.attach(SERVO_PIN);
    servo.write(REST_ANGLE);
    Serial.begin(9600);
}

void wave() {
    int count = random(2, 5);
    for (int i = 0; i < count; i++) {
        int angle = random(20, 40);
        int speed = random(100, 300);
        servo.write(REST_ANGLE + angle);
        delay(speed);
        servo.write(REST_ANGLE);
        delay(speed);
    }
    servo.write(REST_ANGLE);
}

void loop() {
    if (Serial.available() > 0) {
        char c = Serial.read();
        if (c == 'w') {
            wave();
            Serial.write('k');
        }
    }
}
```

- [ ] Step 2: Arduino IDEでコンパイルが通ることを確認（ハードウェア到着後）

Run: Arduino IDEでボード「Arduino Nano」を選択し、検証（Verify）を実行
Expected: コンパイル成功

- [ ] Step 3: コミット

```bash
git add arduino/ccmadocchi/ccmadocchi.ino
```

---

### Task 6: エンドツーエンド動作確認（ハードウェア到着後）

Files:
- なし（動作確認のみ）

- [ ] Step 1: Arduino IDEでMaker Nanoにスケッチを書き込む

1. Maker NanoをUSB Micro-Bでコンピュータに接続
2. Arduino IDEでボード「Arduino Nano」、プロセッサ「ATmega328P」を選択
3. ポートを選択（macOSでは`/dev/cu.usbmodem*`）
4. スケッチを書き込む

- [ ] Step 2: Arduino IDEのシリアルモニタで動作確認

1. シリアルモニタを開く（9600baud）
2. `w` を送信
3. サーボが動くことを確認

- [ ] Step 3: SG90をMaker Nanoに接続

1. ジャンパーワイヤーで接続: 信号(オレンジ)→D9、VCC(赤)→5V、GND(茶)→GND
2. サーボが初期位置（45度）に動くことを確認

- [ ] Step 4: CLIから動作確認

Run: `ccmadocchi wave`
Expected: 「wave送信: /dev/cu.usbmodemXXXX」が表示され、サーボが動く

- [ ] Step 5: ぬいぐるみの腕をくくりつけて最終確認

1. ぬいぐるみをスタンドに立てる
2. サーボをスタンドの横に固定
3. サーボホーンにぬいぐるみの腕を結束バンドでくくりつける
4. `ccmadocchi wave` で腕がぴこぴこ動くことを確認
5. 動きの角度や速度を調整（`arduino/ccmadocchi/ccmadocchi.ino`のパラメータを変更）
