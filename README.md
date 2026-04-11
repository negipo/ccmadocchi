# ccmadocchi

Claude Codeのタスク完了時に、USB経由でぬいぐるみの腕をサーボモーターで動かすCLIツール。

## アーキテクチャ

Python側でモーションのパラメータ(角度、保持時間、繰り返し回数)をランダム生成し、`angle,hold;angle,hold;...\n`形式のコマンド文字列としてシリアル送信する。Arduino側は受け取ったステップ列を順に実行する汎用的な実行器で、モーション定義は持たない。

## セットアップ

### ハードウェア

- Maker Nano (ATmega328P)
- マイクロサーボ SG-90
- ジャンパーワイヤー (オス-メス)

SG90の接続: 信号(オレンジ)→D9、VCC(赤)→5V、GND(茶)→GND

### Arduino

```
arduino-cli compile --fqbn arduino:avr:nano arduino/ccmadocchi
arduino-cli upload --fqbn arduino:avr:nano --port /dev/cu.usbmodemXXXX arduino/ccmadocchi
```

ポートは`arduino-cli board list`で確認する。

### Python CLI

```
uv tool install --force --reinstall ccmadocchi --from .
```

## 使い方

```
ccmadocchi yo                # 軽い挨拶(1回振り)
ccmadocchi wave              # 興奮した手振り(2-4回の振り)
ccmadocchi love              # 親愛の挨拶(大きく動かして保持)
ccmadocchi sad               # 悲しみの表現(少し動かして長く保持)
```

全コマンド共通オプション:

```
--port /dev/cu.usbmodemXXXX  # ポートを明示指定
--silent                      # 出力を抑制(hook用)
--angle N                     # 角度オフセットを固定
--hold N                      # 保持時間msを固定
```

waveのみ `--count N` で繰り返し回数を指定可能。
