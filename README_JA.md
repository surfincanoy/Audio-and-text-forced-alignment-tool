# オーディオとテキストの強制アライメントツール

## 🌐 言語 / Language

[🇨🇳 中文](README.md) | [🇺🇸 English](README_EN.md) | [🇯🇵 日本語](README_JA.md)

## 📋 プロジェクト概要

このプロジェクトは、オーディオファイルと対応するテキストを正確に整列させ、字幕ファイルを生成する柔軟なテキストタイムスタンプ処理解決を提供します。直接テキスト入力またはテキストファイルからの読み取りをサポートし、出力ファイルはオーディオファイル名に基づいて自動的に命名されます。

## 🗂 核心ファイル

### 主要プログラム

- **`flexible_processor.py`** - 核心プロセッサクラス
- **`text2srt.py`** - CLIコマンドラインツール

## 🎯 機能特性

### 1. 句読点記号テキスト入力（デフォルト）

- ✅ **直接テキスト文字列入力**
- ✅ **テキストファイルパスからの読み取り**

### 2. スマートファイル命名

- ✅ **オーディオファイル名による出力の自動命名**
- ✅ **カスタム出力ファイル名のサポート**

### 3. CLIコマンドラインツール

- ✅ **完全なコマンドラインインターフェース**
- ✅ **すべてのプロセッサ機能のサポート**
- ✅ **柔軟なパラメータ設定**

## 🚀 クイックスタート

### CLIツール使用（推奨）

> 💡 **多言語サポート**：このプロジェクトは [🇺🇸 English](README_EN.md) と [🇯🇵 日本語](README_JA.md) ドキュメントをサポートします

#### 基本使い方

```bash
# 直接テキスト入力（オーディオファイル所在ディレクトリへ出力）
uv run text2srt.py -t "これはテストテキストです。2つの文を含んでいます！" -a 1-1.mp3

# テキストファイルから読み取り
uv run text2srt.py -t text.txt -a audio.mp3

# 出力ディレクトリを指定
uv run text2srt.py -t "テキスト内容" -a audio.mp3 -o ./output
```

#### 高度な使い方

```bash
# 句読点記号分割モードを使用
uv run text2srt.py -t text.txt -a audio.mp3 -p "、。！？"

# 言語をカスタマイズ
uv run text2srt.py -t text.txt -a audio.mp3 -l Japanese

# 確認をスキップして直接処理
uv run text2srt.py -t text.txt -a audio.mp3 -y
```

### CLIパラメータ説明

| パラメータ            | 説明                                   | 必須 | デフォルト                         |
| --------------------- | -------------------------------------- | ---- | ---------------------------------- |
| `-t, --text`        | テキスト内容またはテキストファイルパス | ✅   | -                                  |
| `-a, --audio`       | オーディオファイルパス                 | ✅   | -                                  |
| `-o, --output`      | 出力ディレクトリパス                   | ❌   | オーディオファイル所在ディレクトリ |
| `-p, --punctuation` | カスタム分割句読点                     | ❌   | 、。！？                           |
| `-l, --language`    | オーディオ言語                         | ❌   | Japanese                           |
| `-y, --yes`         | 確認をスキップして直接処理             | ❌   | False                              |

### Python API使用

```python
from flexible_processor import FlexibleTextTimestampProcessor

# プロセッサを作成
processor = FlexibleTextTimestampProcessor()

# テキストとオーディオを処理
result = processor.process(
    text_input="あなたのテキスト内容",  # 直接テキスト入力
    audio_path="1-1.mp3"        # オーディオファイル
)

# 自動生成：
# - 1-1.json (完全な結果)
# - 1-1_word.srt (単語レベル字幕)
# - 1-1_sentence.srt (文レベル字幕)
```

## 📖 分割モード

### 1. 句読点記号テキスト分割（推奨）

これはデフォルトのモードです。

#### 使用例

```bash
uv run text2srt.py -t text.txt -a audio.mp3
```

- ✅ **句読点記号による精密な分割**
- ✅ **タイムスタンプマッチングがより正確**
- ✅ **日本語、中国語、英語などのテキストに適している**

### 2. カスタム句読点記号分割

カスタム句読点記号で分割粒度を調整できます。

#### 使用例

```bash
# より詳細な分割
uv run text2srt.py -t text.txt -a audio.mp3 -p "、。！？《》"

# 文末句読点記号のみで分割
uv run text2srt.py -t text.txt -a audio.mp3 -p "。！？"
```

## 📁 出力ファイル説明

### 自動命名ルール

- オーディオファイル：`1-1.mp3`
- 出力ファイル：
  - `1-1.json` - 完全な処理結果
  - `1-1_word.srt` - 単語レベル字幕
  - `1-1_sentence.srt` - 文レベル字幕

### 出力ディレクトリの指定

```bash
uv run text2srt.py -t text.txt -a audio.mp3 -o ./results
# 出力先：./results/1-1.json, ./results/1-1_word.srt, ./results/1-1_sentence.srt
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

- **単語レベルSRT**：各単語に1つのタイムスタンプ、精密な分析に適している
- **文レベルSRT**：各文に1つのタイムスタンプ、通常の字幕に適している

## 🚀 実行例

```bash
# Pythonサンプルを実行
uv run flexible_processor.py

# CLIヘルプを表示
uv run text2srt.py --help

# クイックテスト
uv run text2srt.py -t "テストテキスト" -a 1-1.mp3 -y
```

## 📚 使用例

### 1. ビデオ字幕作成

```bash
# 日本語のビデオに字幕を作成
uv run text2srt.py -t "世界で一番有名な富士山の絵、葛飾北斉。" -a video_audio.mp3 -l Japanese -o ./subtitles

# 英語の学習教材を作成
uv run text2srt.py -t "This is a sentence for learning." -a lesson_audio.mp3 -l English -o ./learning_materials
```

### 2. ポッドキャストトランスクリプション

```bash
# 日本語のポッドキャストを文字起こし
uv run text2srt.py -t podcast_script.txt -a podcast_audio.mp3 -l Japanese -o ./podcast_transcription

# 中国語のトランスクリプション
uv run text2srt.py -t 中文内容 -a chinese_audio.mp3 -l Chinese -o ./chinese_transcription
```

### 3. バッチ処理

```bash
# バッチ処理スクリプトの作成
for audio in *.mp3; do
  text_file="${audio%.mp3}.txt"
  if [ -f "$text_file" ]; then
    uv run text2srt.py -t "$text_file" -a "$audio" -y
  fi
done
```

### 4. 多言語処理

```bash
# 日本語テキスト
uv run text2srt.py -t japanese.txt -a japanese_audio.mp3 -l Japanese -y

# 中国語テキスト
uv run text2srt.py -t chinese.txt -a chinese_audio.mp3 -l Chinese -y

# 英語テキスト
uv run text2srt.py -t english.txt -a english_audio.mp3 -l English -y
```

## 📚 JSON結果フォーマット

```json
{
  "segments": [
    {
      "text": "テキスト内容",
      "start_time": 0.96,
      "end_time": 7.84,
      "words": [
        {
          "text": "世界",
          "start_time": 0.96,
          "end_time": 1.52
        }
      ],
      "match_score": 1.0,
      "segment_type": "sentence"
    }
  ],
  "statistics": {
    "total_segments": 10,
    "total_words": 151,
    "matched_segments": 10,
    "total_duration": 82.72,
    "split_mode": "punctuation",
    "punctuation_used": "、。！？"
  },
  "output_files": {
    "json": "1-1.json",
    "word_srt": "1-1_word.srt",
    "sentence_srt": "1-1_sentence.srt"
  },
  "raw_data": {
    "text_segments": [...],
    "word_timestamps": [...]
  }
}
```

### SRTフォーマット

- **単語レベルSRT**：各単語に正確なタイムスタンプ、精密な分析に適している
- **文レベルSRT**：各文に適切なタイムスタンプ、通常の字幕に適している

## ⚙️ 依存関係

- Python 3.8+
- PyTorch
- qwen-asr
- CUDA対応GPUおよびCPU

## ⚠️ 注意事項

1. **ファイルエンコーディング**：テキストファイルはUTF-8エンコーディングを使用してください
2. **オーディオフォーマット**：一般的なオーディオフォーマット（mp3, wav, m4aなど）をサポート
3. **オーディオマッチング**：オーディオとテキスト内容が一致している必要があります
4. **GPU要件**：CUDA対応GPUが推奨ですが、CPUもサポートされています
5. **ファイル命名**：出力ファイルは自動生成されます、名前の競合を避けてください

## 🎯 アプリケーションシーン

- **ビデオ字幕作成** - 高精度な時間整列字幕の迅速生成
- **言語学習教材** - タイムスタンプ付き学習教材の作成
- **音声認識検証** - ASR結果の正確性の検証
- **コンテンツ分析** - 音声コンテンツの詳細な分析
- **ポッドキャストトランスクリプション** - ポッドキャスト用の字幕と索引の作成
- **マルチメディア処理** - 複数言語でのテキスト処理対応

## 🧧 トラブルシューティング

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

---

## 🤖 オープンソースプロジェクトの引用

### 1. コアエンジン

**Qwen3-ASR**: https://github.com/QwenLM/Qwen3-ASR

- オーディオとテキストの強制整列用エンジン
- 複数言語の正確なタイムスタンプ抽出をサポート
- 高品質な単語レベルタイムスタンプ整列を提供

### 2. モデルファイル

**Qwen3-ForcedAligner-0.6B**: https://huggingface.co/Qwen/Qwen3-ForcedAligner-0.6B

- 高性能な強制整列モデル
- 日本語、中国語、英語など複数言語をサポート
- 秒精度な単語レベルタイムスタンプ整列を提供

### 3. モデルエコシステム

**Hugging Face Qwen**: https://huggingface.co/Qwen

- Qwenシリーズの全モデルとリソースを含む
- モデルのダウンロード、設定と使用ガイドを提供
- 包括的なモデルライブラリとコミュニティサポート

## ⚙️ モデル設定

このプロジェクトでは、以下のモデル設定を使用しています：

```json
{
  "model": "Qwen/Qwen3-ForcedAligner-0.6B",
  "dtype": "bfloat16",
  "device": "cuda:0"
}
```

## 🏗️ 技術アーキテクチャ

このプロジェクトは、Qwen3-ASRとQwen3-ForcedAligner-0.6Bを使用して構築されています：

- **アーキテクチャ**: Transformerベースの強制整列
- **精度**: 高精度な単語レベルタイムスタンプ整列
- **言語サポート**: 日本語、中国語、英語などの複数言語
- **入力形式**: オーディオファイル + 対応テキスト
- **出力形式**: 単語レベル/文レベルタイムスタンプ + SRT字幕

---

このプロジェクトは、使いやすいCLIツールと柔軟なPython APIを含む完全なテキストタイムスタンプ処理ソリューションを提供し、様々な字幕作成とオーディオ処理シーンに適しています。オープンソースのQwen3-ASRプロジェクトに基づき、優秀なQwen3-ForcedAligner-0.6Bモデルを活用して、複数言語をサポートする高品質なテキストタイムスタンプ処理ソリューションを提供します！🎉
