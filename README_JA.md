# テキストタイムスタンプ処理ツール

## 🌐 Language / 言語

[🇨🇳 中文](README.md) | [🇺🇸 English](README_EN.md) | [🇯🇵 日本語](README_JA.md)

## プロジェクト概要

このプロジェクトは、オーディオファイルと対応するテキストを正確に整列させ、字幕ファイルを生成する柔軟なテキストタイムスタンプ処理ソリューションを提供します。直接テキスト入力またはテキストファイルからの読み取りをサポートし、出力ファイルはオーディオファイル名に基づいて自動的に命名されます。

## コアファイル

### 主要プログラム

- **`flexible_processor.py`** - コアプロセッサクラス
- **`text2srt.py`** - CLIコマンドラインツール

## 🎯 機能特性

### 1. 柔軟なテキスト入力

- ✅ **直接テキスト文字列入力**
- ✅ **テキストファイルパスからの読み取り**

### 2. スマートファイル命名

- ✅ **オーディオファイル名で出力を自動命名**
- ✅ **カスタム出力ファイル名をサポート**

### 3. CLIコマンドラインツール

- ✅ **完全なコマンドラインインターフェース**
- ✅ **すべてのプロセッサ機能をサポート**
- ✅ **柔軟なパラメータ設定**

## 🚀 クイックスタート

### CLIツール使用（推奨）

> 💡 **多言語サポート**：このプロジェクトは [🇨🇳 中文](README.md) と [🇺🇸 English](README_EN.md) ドキュメントをサポートしています

#### 基本使用法

```bash
# 直接テキスト入力（オーディオファイルディレクトリに出力）
uv run text2srt.py -t "これはテストテキストです。二つの文が含まれています！" -a 1-1.mp3

# テキストファイルから読み取り
uv run text2srt.py -t text.txt -a audio.mp3

# 出力ディレクトリを指定
uv run text2srt.py -t "テキスト内容" -a audio.mp3 -o ./output
```

#### 高度な使用法

```bash
# 句読点分割モードを使用
uv run text2srt.py -t text.txt -a audio.mp3 -m punctuation -p "、。！？"

# カスタム言語
uv run text2srt.py -t text.txt -a audio.mp3 -l Chinese

# 確認をスキップして直接処理
uv run text2srt.py -t text.txt -a audio.mp3 -y
```

### CLIパラメータ説明

| パラメータ            | 説明                                   | 必須 | デフォルト                     |
| --------------------- | -------------------------------------- | ---- | ------------------------------ |
| `-t, --text`        | テキスト内容またはテキストファイルパス | ✅   | -                              |
| `-a, --audio`       | オーディオファイルパス                 | ✅   | -                              |
| `-o, --output`      | 出力ディレクトリパス                   | ❌   | オーディオファイルディレクトリ |
| `-m, --mode`        | 分割モード (intelligent/punctuation)   | ❌   | intelligent                    |
| `-p, --punctuation` | カスタム分割句読点                     | ❌   | 、。！？                       |
| `-l, --language`    | オーディオ言語                         | ❌   | Japanese                       |
| `-y, --yes`         | 確認をスキップして直接処理             | ❌   | False                          |

### Python API使用

```python
from flexible_processor import FlexibleTextTimestampProcessor

# プロセッサを作成
processor = FlexibleTextTimestampProcessor()

# テキストとオーディオを処理
result = processor.process(
    text_input="あなたのテキスト内容",  # 直接テキスト入力
    audio_path="1-1.mp3"               # オーディオファイル
)

# 自動生成：
# - 1-1.json (完全な結果)
# - 1-1_word.srt (単語レベル字幕)
# - 1-1_sentence.srt (文レベル字幕)
```

## 📖 分割モード

### 1. インテリジェント分割（推奨）

```bash
uv run text2srt.py -t text.txt -a audio.mp3 -m intelligent
```

- 意味的な文で分割
- 意味的整合性を維持
- 標準的な字幕作成に適している

### 2. カスタム句読点分割

```bash
uv run text2srt.py -t text.txt -a audio.mp3 -m punctuation -p "。！？"
```

- 指定された句読点で分割
- カスタマイズ可能な分割粒度
- 特殊な要件に適している

## 📁 出力ファイル説明

### 自動命名ルール

- オーディオファイル：`1-1.mp3`
- 出力ファイル：
  - `1-1.json` - 完全な処理結果
  - `1-1_word.srt` - 単語レベル字幕
  - `1-1_sentence.srt` - 文レベル字幕

### 出力ディレクトリを指定

```bash
uv run text2srt.py -t text.txt -a audio.mp3 -o ./results
# 出力先：./results/1-1.json, ./results/1-1_word.srt, ./results/1-1_sentence.srt
```

## 💡 使用例

### 1. ビデオ字幕作成

```bash
# ビデオの字幕を作成
uv run text2srt.py -t video_script.txt -a video_audio.mp3 -o ./subtitles

# 学習教材を作成
uv run text2srt.py -t "今日は天気がいいです。公園を散歩しましょう。" -a japanese_audio.mp3 -l Japanese
```

### 2. 言語学習教材

```bash
# 日本語テキスト
uv run text2srt.py -t japanese.txt -a japanese_audio.mp3 -l Japanese

# 中国語テキスト
uv run text2srt.py -t chinese.txt -a chinese_audio.mp3 -l Chinese

# 英語テキスト
uv run text2srt.py -t english.txt -a english_audio.mp3 -l English
```

### 3. バッチ処理

```bash
# バッチ処理スクリプトを作成
for audio in *.mp3; do
  text_file="${audio%.mp3}.txt"
  if [ -f "$text_file" ]; then
    uv run text2srt.py -t "$text_file" -a "$audio" -y
  fi
done
```

## 🏃 実行例

```bash
# Python例を実行
uv run text2srt.py

# CLIヘルプを表示
uv run text2srt.py --help

# クイックテスト
uv run text2srt.py -t "テストテキスト" -a 1-1.mp3 -y
```

## 📊 出力フォーマット

### JSON結果フォーマット

```json
{
  "segments": [
    {
      "text": "テキスト内容",
      "start_time": 0.96,
      "end_time": 7.84,
      "words": [...],
      "match_score": 1.0
    }
  ],
  "statistics": {
    "total_segments": 10,
    "total_words": 151,
    "matched_segments": 10
  },
  "output_files": {
    "json": "1-1.json",
    "word_srt": "1-1_word.srt",
    "sentence_srt": "1-1_sentence.srt"
  }
}
```

### SRTフォーマット

- **単語レベルSRT**：単語ごとのタイムスタンプ、精密な分析に適している
- **文レベルSRT**：文ごとのタイムスタンプ、通常の字幕に適している

## ⚙️ 依存関係

- Python 3.8+
- PyTorch
- qwen-asr
- CUDAサポートGPUまたはCPU

## ⚠️ 注意事項

1. **ファイルエンコーディング**：テキストファイルはUTF-8エンコーディングを使用してください
2. **オーディオフォーマット**：一般的なオーディオフォーマット（mp3, wav, m4aなど）をサポート
3. **オーディオマッチング**：オーディオとテキスト内容が一致している必要があります
4. **GPU要件**：CUDAサポートGPUが推奨ですが、CPUもサポートされています
5. **ファイル命名**：出力ファイルは自動生成されます、名前の競合を避けてください

## 🎯 アプリケーションシーン

- **ビデオ字幕作成** - 正確な時間整列字幕を迅速生成
- **言語学習** - タイムスタンプ付き学習教材を作成
- **音声認識検証** - ASR結果の正確性を検証
- **コンテンツ分析** - 音声コンテンツの詳細な分析
- **ポッドキャストトランスクリプション** - ポッドキャストの字幕と索引を作成

## 🔧 トラブルシューティング

### 一般的な問題

1. **モデル読み込み失敗**

   ```
   [ERROR] モデルを読み込めません
   ```
   解決策：CUDAとGPUメモリを確認
2. **サポートされていないオーディオファイル**

   ```
   [ERROR] オーディオファイルが存在しません
   ```
   解決策：ファイルパスとフォーマットを確認
3. **テキスト読み込み失敗**

   ```
   [ERROR] ファイルの読み込みに失敗しました
   ```
   解決策：テキストファイルがUTF-8エンコーディングを使用していることを確認
4. **出力ディレクトリ権限**

   ```
   [ERROR] 出力ディレクトリを作成できません
   ```
   解決策：ディレクトリ権限を確認するか、他のディレクトリを選択
