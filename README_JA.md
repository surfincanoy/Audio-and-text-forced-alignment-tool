# 音声テキスト強制アライメントツール

## 🌐 言語 / Language

[🇨🇳 中文](README.md) | [🇺🇸 English](README_EN.md) | [🇯🇵 日本語](README_JA.md)

Qwen3-ForcedAligner ベースのインテリジェントメディアファイルタイムスタンプ処理ツール。テキストと動画・音声ファイルのタイムスタンプ自動マッチングをサポートし、正確な単語レベルと文レベルの字幕を生成します。

## 🌟 主な機能

- ✅ **マルチフォーマット対応**：音声ファイル (.mp3, .wav, .m4a, .aac, .ogg, .flac) と動画ファイル (.mp4, .avi, .mov, .mkv, .flv, .wmv, .webm)
- ✅ **スマートテキスト分割**：カスタム句読点によるテキスト分割をサポート
- ✅ **マルチフォーマット出力**：JSON、単語レベルSRT、文レベルSRTファイルを生成

## 📦 依存関係のインストール

```bash
# コア依存関係のインストール
pip install torch qwen-asr

# オプション：動画処理用にFFmpegをインストール
# Windows: ダウンロードしてインストール https://ffmpeg.org/download.html
# macOS: brew install ffmpeg
# Ubuntu: sudo apt-get install ffmpeg
```

## 🚀 クイックスタート

### 1. コマンドライン使用（仮想環境の使用を推奨）

```bash
# 音声ファイルの処理
uv run text2srt.py -t "テキスト内容" -a audio.mp3

# ファイルからテキストを読み込んで音声を処理
uv run text2srt.py -t text.txt -a audio.mp3

# 動画ファイルの処理（自動で音声に変換）
uv run text2srt.py -t "動画字幕テキスト" -v video.mp4

# 言語を指定
uv run text2srt.py -t text.txt -a audio.mp3 -l Japanese
```

### 2. コード内での使用

```python
from flexible_processor import FlexibleTextTimestampProcessor

# プロセッサーを作成
processor = FlexibleTextTimestampProcessor()

# 音声ファイルの処理
result = processor.process(
    text_input="テキスト内容",
    audio_path="audio.mp3",
    language="Japanese"
)

# 動画ファイルの処理
result = processor.process_media_file(
    media_path="video.mp4",
    text_input="動画字幕テキスト"
)

if result:
    print(f"{len(result['output_files'])}個のファイルが生成されました")
    print(f"マッチング率: {result['statistics']['matched_segments']}/{result['statistics']['total_segments']}")
```

## 📁 出力ファイル

処理完了後、3つのファイルが生成されます：

- `{ファイル名}.json` - 完全なJSON結果データ
- `{ファイル名}_word.srt` - 単語レベルSRT字幕（各単語を個別表示）
- `{ファイル名}_sentence.srt` - 文レベルSRT字幕（文単位で表示）

## 🔧 高度な設定

### カスタム句読点による分割

```python
processor = FlexibleTextTimestampProcessor()
processor.set_custom_punctuation("、。！？《》")  # カスタム分割句読点
```

### サポート言語

- Japanese (日本語), Chinese (中国語), English (英語), etc.

## 🎯 使用例

### 基本例

```python
from flexible_processor import FlexibleTextTimestampProcessor

# サンプルテキスト
text = """世界で一番有名な富士山の絵、葛飾北斉。1998年にアメリカの雑誌《ライフ》がこの千年の間の世界のすごい人100人を選びました。"""

# プロセッサー作成
processor = FlexibleTextTimestampProcessor()

# 処理実行
result = processor.process(text, "audio.mp3")

# 統計情報出力
stats = result['statistics']
print(f"セグメント数: {stats['total_segments']}")
print(f"単語数: {stats['total_words']}")
print(f"マッチング率: {stats['matched_segments']}/{stats['total_segments']}")
```

### 動画処理例

```python
# 動画ファイル処理
result = processor.process_media_file(
    media_path="video.mp4",
    text_input="動画対応テキスト内容"
)

# 自動処理フロー：動画 → 音声 → タイムスタンプ → 字幕
```

### バッチ処理例

```python
import os
from pathlib import Path

# ディレクトリ内の全音声ファイルをバッチ処理
audio_dir = Path("audio_files")
text_dir = Path("text_files")

for audio_file in audio_dir.glob("*.mp3"):
    # 対応するテキストファイル
    text_file = text_dir / f"{audio_file.stem}.txt"
  
    if text_file.exists():
        result = processor.process_media_file(
            media_path=str(audio_file),
            text_input=str(text_file)
        )
        print(f"処理完了: {audio_file.name}")
```

## ⚠️ 注意事項

1. **モデルパス**：Qwen\Qwen3-ForcedAligner-0.6B
2. **GPUサポート**：CUDAを自動検出、GPUがある場合に自動使用
3. **音声品質**：クリアでバックグラウンドノイズのない音声または動画を推奨
4. **テキストマッチング**：最高の効果を得るため、テキスト内容と音声内容が一致している必要があります
5. **FFmpegパス**：FFmpegがシステムPATHにあることを確認（動画処理に必要）

## 📜 ライセンス

MIT License

## 🔗 関連リンク

- 里官方开源プロジェクト             [Qwen3-ASR](https://github.com/QwenLM/Qwen3-ASR)
- モデルダウンロード（huggingface）[Qwen3-ForcedAligner](https://huggingface.co/Qwen/Qwen3-ForcedAligner-0.6B)
- モデルダウンロード（modelscope）[Qwen3-ForcedAligner](https://www.modelscope.cn/models/Qwen/Qwen3-ForcedAligner-0.6B)
- [FFmpeg公式サイト](https://ffmpeg.org/)
- [PyTorch](https://pytorch.org/)
