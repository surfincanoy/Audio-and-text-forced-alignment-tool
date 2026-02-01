# Audio-Text Forced Alignment Tool

## 🌐 Language / 语言

[🇨🇳 中文](README.md) | [🇺🇸 English](README_EN.md) | [🇯🇵 日本語](README_JA.md)

An intelligent media file timestamp processing tool based on Qwen3-ForcedAligner. Supports automatic timestamp matching between text and video/audio files, generating accurate word-level and sentence-level subtitles.

## 🌟 Key Features

- ✅ **Multi-format Support**: Audio files (.mp3, .wav, .m4a, .aac, .ogg, .flac) and video files (.mp4, .avi, .mov, .mkv, .flv, .wmv, .webm)
- ✅ **Smart Text Splitting**: Support custom punctuation for text segmentation
- ✅ **Multi-format Output**: Generate JSON, word-level SRT, sentence-level SRT files

## 📦 Install Dependencies

```bash
# Install core dependencies
pip install torch qwen-asr

# Optional: Install FFmpeg for video processing
# Windows: Download and install https://ffmpeg.org/download.html
# macOS: brew install ffmpeg
# Ubuntu: sudo apt-get install ffmpeg
```

## 🚀 Quick Start

### 1. Command Line Usage (virtual environment recommended)

```bash
# Process audio file
uv run text2srt.py -t "Your text content" -a audio.mp3

# Read text from file and process audio
uv run text2srt.py -t text.txt -a audio.mp3

# Process video file (automatically convert to audio)
uv run text2srt.py -t "Video subtitle text" -v video.mp4

# Specify language
uv run text2srt.py -t text.txt -a audio.mp3 -l Japanese
```

### 2. Usage in Code

```python
from flexible_processor import FlexibleTextTimestampProcessor

# Create processor
processor = FlexibleTextTimestampProcessor()

# Process audio file
result = processor.process(
    text_input="Your text content",
    audio_path="audio.mp3",
    language="Japanese"
)

# Process video file
result = processor.process_media_file(
    media_path="video.mp4",
    text_input="Video subtitle text"
)

if result:
    print(f"Generated {len(result['output_files'])} files")
    print(f"Matching rate: {result['statistics']['matched_segments']}/{result['statistics']['total_segments']}")
```

## 📁 Output Files

After processing completion, three files will be generated:

- `{filename}.json` - Complete JSON result data
- `{filename}_word.srt` - Word-level SRT subtitles (each word displayed separately)
- `{filename}_sentence.srt` - Sentence-level SRT subtitles (displayed by sentence)

## 🔧 Advanced Configuration

### Custom Punctuation Splitting

```python
processor = FlexibleTextTimestampProcessor()
processor.set_custom_punctuation("、。！？《》")  # Custom splitting punctuation
```

### Supported Languages

- Japanese (日本語), Chinese (中文), English (英语), etc.

## 🎯 Usage Examples

### Basic Example

```python
from flexible_processor import FlexibleTextTimestampProcessor

# Sample text
text = """世界で一番有名な富士山の絵、葛飾北斉。1998年にアメリカの雑誌《ライフ》がこの千年の間の世界のすごい人100人を選びました。"""

# Create processor
processor = FlexibleTextTimestampProcessor()

# Process
result = processor.process(text, "audio.mp3")

# Output statistics
stats = result['statistics']
print(f"Segments: {stats['total_segments']}")
print(f"Words: {stats['total_words']}")
print(f"Matching rate: {stats['matched_segments']}/{stats['total_segments']}")
```

### Video Processing Example

```python
# Process video file
result = processor.process_media_file(
    media_path="video.mp4",
    text_input="Video corresponding text content"
)

# Automatic processing flow: video → audio → timestamps → subtitles
```

### Batch Processing Example

```python
import os
from pathlib import Path

# Batch process all audio files in directory
audio_dir = Path("audio_files")
text_dir = Path("text_files")

for audio_file in audio_dir.glob("*.mp3"):
    # Corresponding text file
    text_file = text_dir / f"{audio_file.stem}.txt"
  
    if text_file.exists():
        result = processor.process_media_file(
            media_path=str(audio_file),
            text_input=str(text_file)
        )
        print(f"Processing completed: {audio_file.name}")
```

## ⚠️ Important Notes

1. **Model Path**: Qwen\Qwen3-ForcedAligner-0.6B
2. **GPU Support**: Auto-detect CUDA, automatically use when GPU available
3. **Audio Quality**: Recommend clear audio without background noise or video
4. **Text Matching**: Text content should match audio content for best results
5. **FFmpeg Path**: Ensure FFmpeg is in system PATH (required for video processing)

## 📜 License

MIT License

## 🔗 Related Links

- 里官方开源项目             [Qwen3-ASR](https://github.com/QwenLM/Qwen3-ASR)
- Model download (huggingface)[Qwen3-ForcedAligner](https://huggingface.co/Qwen/Qwen3-ForcedAligner-0.6B)
- Model download (modelscope)[Qwen3-ForcedAligner](https://www.modelscope.cn/models/Qwen/Qwen3-ForcedAligner-0.6B)
- [FFmpeg Official Website](https://ffmpeg.org/)
- [PyTorch](https://pytorch.org/)
