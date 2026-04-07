# ccmadocchi

Claude Codeのタスク完了時に、USB経由でぬいぐるみの腕をサーボモーターで動かすCLIツール。

## セットアップ

### ハードウェア

- Maker Nano (ATmega328P)
- マイクロサーボ SG-90
- ジャンパーワイヤー (オス-メス)

SG90の接続: 信号(オレンジ)→D9、VCC(赤)→5V、GND(茶)→GND

### Arduino

Arduino IDEで `arduino/ccmadocchi/ccmadocchi.ino` をMaker Nanoに書き込む。

### Python CLI

```
uv tool install .
```

## 使い方

```
ccmadocchi wave
```

ポートを明示的に指定する場合:

```
ccmadocchi wave --port /dev/cu.usbmodemXXXX
```
