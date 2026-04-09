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
ccmadocchi wave              # 興奮した手振り（2〜4回ランダム）
ccmadocchi love              # 親愛の挨拶（ゆっくり上げて戻す）
ccmadocchi sad               # 悲しみの表現（少し上げてしばらく待つ）
```

ポートを明示的に指定する場合:

```
ccmadocchi wave --port /dev/cu.usbmodemXXXX
```
