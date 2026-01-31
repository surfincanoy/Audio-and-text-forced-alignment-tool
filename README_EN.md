# Audio and text forced alignment tool

## 🌐 Language / 言語

[🇨🇳 中文](README.md) | [🇺🇸 English](README_EN.md) | [🇯🇵 日本語](README_JA.md)

## Project Overview

This project provides a flexible text timestamp processing solution that can precisely align audio files with corresponding text to generate subtitle files. It supports direct text input or reading from text files, with output files automatically named according to the audio filename.

## Core Files

### Main Programs

- **`flexible_processor.py`** - Core processor class
- **`text2srt.py`** - CLI command line tool

## 🎯 Features

### 1. Flexible Text Input

- ✅ **Direct text string input**
- ✅ **Read from text file path**

### 2. Smart File Naming

- ✅ **Auto-name outputs by audio filename**
- ✅ **Support custom output filenames**

### 3. CLI Command Line Tool

- ✅ **Complete command line interface**
- ✅ **Support all processor features**
- ✅ **Flexible parameter configuration**

## 🚀 Quick Start

### CLI Tool Usage (Recommended)

> 💡 **Multi-language Support**: This project supports [🇨🇳 Chinese](README.md) and [🇯🇵 日本語](README_JA.md) documentation

#### Basic Usage

```bash
# Direct text input (output to audio file directory)
uv run text2srt.py -t "This is test text. Contains two sentences!" -a 1-1.mp3

# Read from text file
uv run text2srt.py -t text.txt -a audio.mp3

# Specify output directory
uv run text2srt.py -t "Text content" -a audio.mp3 -o ./output
```

#### Advanced Usage

```bash
# Use punctuation splitting mode
uv run text2srt.py -t text.txt -a audio.mp3 -m punctuation -p ".,!?"

# Custom language
uv run text2srt.py -t text.txt -a audio.mp3 -l English

# Skip confirmation and process directly
uv run text2srt.py -t text.txt -a audio.mp3 -y
```

### CLI Parameter Description

| Parameter             | Description                              | Required | Default              |
| --------------------- | ---------------------------------------- | -------- | -------------------- |
| `-t, --text`        | Text content or text file path           | ✅       | -                    |
| `-a, --audio`       | Audio file path                          | ✅       | -                    |
| `-o, --output`      | Output directory path                    | ❌       | Audio file directory |
| `-m, --mode`        | Splitting mode (intelligent/punctuation) | ❌       | intelligent          |
| `-p, --punctuation` | Custom splitting punctuation             | ❌       | 、。！？             |
| `-l, --language`    | Audio language                           | ❌       | Japanese             |
| `-y, --yes`         | Skip confirmation and process directly   | ❌       | False                |

### Python API Usage

```python
from flexible_processor import FlexibleTextTimestampProcessor

# Create processor
processor = FlexibleTextTimestampProcessor()

# Process text and audio
result = processor.process(
    text_input="Your text content",  # Direct text input
    audio_path="1-1.mp3"           # Audio file
)

# Automatically generated:
# - 1-1.json (complete results)
# - 1-1_word.srt (word-level subtitles)
# - 1-1_sentence.srt (sentence-level subtitles)
```

## 📖 Splitting Modes

### 1. Intelligent Splitting (Recommended)

```bash
uv run text2srt.py -t text.txt -a audio.mp3 -m intelligent
```

- Splits by semantic sentences
- Maintains semantic integrity
- Suitable for standard subtitle production

### 2. Custom Punctuation Splitting

```bash
uv run text2srt.py -t text.txt -a audio.mp3 -m punctuation -p ".!?"
```

- Splits by specified punctuation
- Customizable splitting granularity
- Suitable for special requirements

## 📁 Output File Description

### Auto Naming Rules

- Audio file: `1-1.mp3`
- Output files:
  - `1-1.json` - Complete processing results
  - `1-1_word.srt` - Word-level subtitles
  - `1-1_sentence.srt` - Sentence-level subtitles

### Specify Output Directory

```bash
uv run text2srt.py -t text.txt -a audio.mp3 -o ./results
# Output to: ./results/1-1.json, ./results/1-1_word.srt, ./results/1-1_sentence.srt
```

## 💡 Usage Examples

### 1. Video Subtitle Production

```bash
# Create subtitles for video
uv run text2srt.py -t video_script.txt -a video_audio.mp3 -o ./subtitles

# Create learning materials
uv run text2srt.py -t "The weather is nice today. Let's go for a walk in the park." -a english_audio.mp3 -l English
```

### 2. Language Learning Materials

```bash
# Japanese text
uv run text2srt.py -t japanese.txt -a japanese_audio.mp3 -l Japanese

# Chinese text
uv run text2srt.py -t chinese.txt -a chinese_audio.mp3 -l Chinese

# English text
uv run text2srt.py -t english.txt -a english_audio.mp3 -l English
```

### 3. Batch Processing

```bash
# Create batch processing script
for audio in *.mp3; do
  text_file="${audio%.mp3}.txt"
  if [ -f "$text_file" ]; then
    uv run text2srt.py -t "$text_file" -a "$audio" -y
  fi
done
```

## 🏃 Running Examples

```bash
# Run Python examples
uv run text2srt.py

# View CLI help
uv run text2srt.py --help

# Quick test
uv run text2srt.py -t "Test text" -a 1-1.mp3 -y
```

## 📊 Output Format

### JSON Result Format

```json
{
  "segments": [
    {
      "text": "Text content",
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

### SRT Format

- **Word-level SRT**: One timestamp per word, suitable for precise analysis
- **Sentence-level SRT**: One timestamp per sentence, suitable for regular subtitles

## ⚙️ Dependencies

- Python 3.8+
- PyTorch
- qwen-asr
- CUDA-supported GPU or CPU

## ⚠️ Important Notes

1. **File Encoding**: Please use UTF-8 encoding for text files
2. **Audio Format**: Supports common audio formats (mp3, wav, m4a, etc.)
3. **Audio Matching**: Audio and text content need to match
4. **GPU Requirement**: CUDA-supported GPU is recommended, CPU is also supported
5. **File Naming**: Output files are automatically generated, avoid naming conflicts

## 🎯 Application Scenarios

- **Video Subtitle Production** - Quickly generate accurately time-aligned subtitles
- **Language Learning** - Create timestamped learning materials
- **Speech Recognition Verification** - Verify ASR result accuracy
- **Content Analysis** - Fine-grained analysis of speech content
- **Podcast Transcription** - Create subtitles and indexes for podcasts

## 🔧 Troubleshooting

### Common Issues

1. **Model Loading Failed**

   ```
   [ERROR] Cannot load model
   ```
   Solution: Check CUDA and GPU memory
2. **Unsupported Audio File**

   ```
   [ERROR] Audio file does not exist
   ```
   Solution: Check file path and format
3. **Text Reading Failed**

   ```
   [ERROR] Failed to read file
   ```
   Solution: Ensure text file uses UTF-8 encoding
4. **Output Directory Permissions**

   ```
   [ERROR] Cannot create output directory
   ```
   Solution: Check directory permissions or choose another directory


## 🤖 Open Source Projects

### 1. Core Engine
**Qwen3-ASR**: https://github.com/QwenLM/Qwen3-ASR
- Audio-text forced alignment engine
- Supports multiple language precise timestamp extraction
- Provides high-quality word-level timestamp alignment

### 2. Model Files
**Qwen3-ForcedAligner-0.6B**: https://huggingface.co/Qwen/Qwen3-ForcedAligner-0.6B
- High-performance forced alignment model
- Supports Japanese, Chinese, English and multiple languages
- Provides accurate word-level timestamp to second precision

### 3. Model Ecosystem
**Hugging Face Qwen**: https://huggingface.co/Qwen
- Complete ecosystem of Qwen series models and resources
- Provides model download, configuration and usage guides
- Comprehensive model library and community support

## ⚙️ Model Configuration

The project uses the following model configuration:
```json
{
  "model": "Qwen/Qwen3-ForcedAligner-0.6B",
  "dtype": "bfloat16",
  "device": "cuda:0"
}
```

## 🏗️ Technical Architecture

This project is built with Qwen3-ASR and Qwen3-ForcedAligner-0.6B:

- **Architecture**: Transformer-based forced alignment
- **Precision**: High-precision word-level timestamp alignment
- **Language Support**: Japanese, Chinese, English and multiple languages
- **Input Format**: Audio file + corresponding text
- **Output Format**: Word-level/sentence-level timestamps + SRT subtitles

---

This project provides a complete text timestamp processing solution, including easy-to-use CLI tools and flexible Python APIs, suitable for various subtitle production and audio processing scenarios. Based on the open-source Qwen3-ASR project and utilizing the excellent Qwen3-ForcedAligner-0.6B model, it provides high-quality text timestamp processing solutions supporting multiple languages.
