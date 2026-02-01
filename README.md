# 音频文本强制对齐工具

## 🌐 语言 / Language

[🇨🇳 中文](README.md) | [🇺🇸 English](README_EN.md) | [🇯🇵 日本語](README_JA.md)

基于 Qwen3-ForcedAligner 的智能媒体文件时间戳处理工具，支持文本与视频及音频文件的时间戳自动匹配，生成精确的字词级和句级字幕。

## 🌟 主要特性

- ✅ **多格式支持**：音频文件 (.mp3, .wav, .m4a, .aac, .ogg, .flac) 和视频文件 (.mp4, .avi, .mov, .mkv, .flv, .wmv, .webm)
- ✅ **智能文本分割**：支持自定义标点符号分割文本
- ✅ **多格式输出**：生成 JSON、字词级 SRT、句级 SRT 文件

## 📦 安装依赖

```bash
# 安装核心依赖
pip install torch qwen-asr

# 可选：安装 FFmpeg 用于视频处理
# Windows: 下载并安装 https://ffmpeg.org/download.html
# macOS: brew install ffmpeg
# Ubuntu: sudo apt-get install ffmpeg
```

## 🚀 快速开始

### 1. 命令行使用（推荐使用虚拟环境）

```bash
# 处理音频文件
uv run text2srt.py -t "你的文本内容" -a audio.mp3

# 从文件读取文本并处理音频
uv run text2srt.py -t text.txt -a audio.mp3

# 处理视频文件（自动转换为音频）
uv run text2srt.py -t "视频字幕文本" -v video.mp4

# 指定语言
uv run text2srt.py -t text.txt -a audio.mp3 -l Japanese
```

### 2. 代码中使用

```python
from flexible_processor import FlexibleTextTimestampProcessor

# 创建处理器
processor = FlexibleTextTimestampProcessor()

# 处理音频文件
result = processor.process(
    text_input="你的文本内容",
    audio_path="audio.mp3",
    language="Japanese"
)

# 处理视频文件
result = processor.process_media_file(
    media_path="video.mp4",
    text_input="视频字幕文本"
)

if result:
    print(f"生成了 {len(result['output_files'])} 个文件")
    print(f"匹配率: {result['statistics']['matched_segments']}/{result['statistics']['total_segments']}")
```

## 📁 输出文件

处理完成后会生成三个文件：

- `{文件名}.json` - 完整的JSON结果数据
- `{文件名}_word.srt` - 字词级SRT字幕（每个词单独显示）
- `{文件名}_sentence.srt` - 句级SRT字幕（按句子显示）

## 🔧 高级配置

### 自定义标点符号分割

```python
processor = FlexibleTextTimestampProcessor()
processor.set_custom_punctuation("、。！？《》")  # 自定义分割标点
```

### 支持的语言

- Japanese (日语), Chinese (中文), English (英语), etc.

## 🎯 使用示例

### 基础示例

```python
from flexible_processor import FlexibleTextTimestampProcessor

# 示例文本
text = """世界で一番有名な富士山の絵、葛飾北斉。1998年にアメリカの雑誌《ライフ》がこの千年の間の世界のすごい人100人を選びました。"""

# 创建处理器
processor = FlexibleTextTimestampProcessor()

# 处理
result = processor.process(text, "audio.mp3")

# 输出统计
stats = result['statistics']
print(f"段落数: {stats['total_segments']}")
print(f"词数: {stats['total_words']}")
print(f"匹配率: {stats['matched_segments']}/{stats['total_segments']}")
```

### 视频处理示例

```python
# 处理视频文件
result = processor.process_media_file(
    media_path="video.mp4",
    text_input="视频对应的文本内容"
)

# 自动处理流程：视频 → 音频 → 时间戳 → 字幕
```

### 批量处理示例

```python
import os
from pathlib import Path

# 批量处理目录中的所有音频文件
audio_dir = Path("audio_files")
text_dir = Path("text_files")

for audio_file in audio_dir.glob("*.mp3"):
    # 对应的文本文件
    text_file = text_dir / f"{audio_file.stem}.txt"
  
    if text_file.exists():
        result = processor.process_media_file(
            media_path=str(audio_file),
            text_input=str(text_file)
        )
        print(f"处理完成: {audio_file.name}")
```

## ⚠️ 注意事项

1. **模型路径**：Qwen\Qwen3-ForcedAligner-0.6B
2. **GPU 支持**：自动检测 CUDA，有 GPU 时会自动使用
3. **音频质量**：建议使用清晰的无背景噪音音频或者视频
4. **文本匹配**：文本内容应与音频内容匹配以获得最佳效果
5. **FFmpeg 路径**：确保 FFmpeg 在系统 PATH 中（视频处理需要）

## 📜 许可证

MIT License

## 🔗 相关链接

- 阿里官方开源项目             [Qwen3-ASR](https://github.com/QwenLM/Qwen3-ASR)
- 模型下载（huggingface）[Qwen3-ForcedAligner](https://huggingface.co/Qwen/Qwen3-ForcedAligner-0.6B)
- 模型下载（modelscope）[Qwen3-ForcedAligner](https://www.modelscope.cn/models/Qwen/Qwen3-ForcedAligner-0.6B)
- [FFmpeg 官网](https://ffmpeg.org/)
- [PyTorch](https://pytorch.org/)
