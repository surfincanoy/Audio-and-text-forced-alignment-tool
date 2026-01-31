# 音文强制对齐工具

## 🌐 语言 / Language

[🇨🇳 中文](README.md) | [🇺🇸 English](README_EN.md) | [🇯🇵 日本語](README_JA.md)

## 项目概述

这个项目提供了一个灵活的文本时间戳处理解决方案，可以将音频文件与对应的文本进行精确对齐，生成字幕文件。支持直接输入文本或从文本文件读取，输出文件自动按音频文件名命名。

## 核心文件

### 主要程序

- **`flexible_processor.py`** - 核心处理器类
- **`text2srt.py`** - CLI命令行工具

## 🎯 功能特性

### 1. 灵活的文本输入

- ✅ **直接输入文本字符串**
- ✅ **从文本文件路径读取**

### 2. 智能文件命名（标点分割默认）

- ✅ **自动按音频文件名命名输出**
- ✅ **支持自定义输出文件名**

### 3. CLI命令行工具

- ✅ **完整的命令行界面**
- ✅ **支持所有处理器功能**
- ✅ **灵活的参数配置**

## 🚀 快速开始

### CLI工具使用（推荐）

> 💡 **多语言支持**：本项目支持 [🇺🇸 English](README_EN.md) 和 [🇯🇵 日本語](README_JA.md) 文档

#### 基本用法

```bash
# 直接输入文本（输出到音频文件所在目录）
uv run text2srt.py -t "这是测试文本。包含两个句子！" -a 1-1.mp3

# 从文本文件读取
uv run text2srt.py -t text.txt -a audio.mp3

# 指定输出目录
uv run text2srt.py -t "文本内容" -a audio.mp3 -o ./output
```

#### 高级用法

```bash
# 使用标点分割模式
uv run text2srt.py -t text.txt -a audio.mp3 -m punctuation -p "、，。！？"

# 自定义语言
uv run text2srt.py -t text.txt -a audio.mp3 -l Chinese

# 跳过确认直接处理
uv run text2srt.py -t text.txt -a audio.mp3 -y
```

### CLI参数说明

| 参数                  | 说明                   | 必需 | 默认值           |
| --------------------- | ---------------------- | ---- | ---------------- |
| `-t, --text`        | 文本内容或文本文件路径 | ✅   | -                |
| `-a, --audio`       | 音频文件路径           | ✅   | -                |
| `-o, --output`      | 输出目录路径           | ❌   | 音频文件所在目录 |
| `-p, --punctuation` | 自定义分割标点         | ❌   | 、。！？         |
| `-l, --language`    | 音频语言               | ❌   | Japanese         |
| `-y, --yes`         | 跳过确认直接处理       | ❌   | False            |

### Python API使用

```python
from flexible_processor import FlexibleTextTimestampProcessor

# 创建处理器
processor = FlexibleTextTimestampProcessor()

# 处理文本和音频
result = processor.process(
    text_input="你的文本内容",  # 直接输入文本
    audio_path="1-1.mp3"        # 音频文件
)

# 自动生成：
# - 1-1.json (完整结果)
# - 1-1_word.srt (字词级字幕)
# - 1-1_sentence.srt (句级字幕)
```

## 📖 分割模式

### 1. 标点符号文本分割（推荐）

```bash
uv run text2srt.py -t text.txt -a audio.mp3 -m punctuation -p "、。！？"
```

- 按标点符号精确分割
- 时间戳匹配更准确
- 适合日语、中文等文本

### 2. 自定义标点分割

```bash
uv run text2srt.py -t text.txt -a audio.mp3 -m punctuation -p "。！？"
```

- 按指定标点符号分割
- 可自定义分割粒度
- 适合特定需求

## 📁 输出文件说明

### 自动命名规则

- 音频文件：`1-1.mp3`
- 输出文件：
  - `1-1.json` - 完整处理结果
  - `1-1_word.srt` - 字词级字幕
  - `1-1_sentence.srt` - 句级字幕

### 指定输出目录

```bash
uv run text2srt.py -t text.txt -a audio.mp3 -o ./results
# 输出到：./results/1-1.json, ./results/1-1_word.srt, ./results/1-1_sentence.srt
```

## 💡 使用示例

### 1. 视频字幕制作

```bash
# 为视频制作字幕
uv run text2srt.py -t video_script.txt -a video_audio.mp3 -o ./subtitles

# 制作学习材料
uv run text2srt.py -t "今天天气很好。我们去公园散步吧。" -a chinese_audio.mp3 -l Chinese
```

### 3. 批量处理

```bash
# 创建批量处理脚本
for audio in *.mp3; do
  text_file="${audio%.mp3}.txt"
  if [ -f "$text_file" ]; then
    uv run text2srt.py -t "$text_file" -a "$audio" -y
  fi
done
```

### 4. 不同语言处理

```bash
text2srt.py# 日语文本
uv run text2srt.py -t japanese.txt -a japanese_audio.mp3 -l Japanese

# 中文文本
uv run text2srt.py -t chinese.txt -a chinese_audio.mp3 -l Chinese

# 英文文本
uv run text2srt.py -t english.txt -a english_audio.mp3 -l English
```

## 🏃 运行示例

```bash
# 运行Python示例
uv run text2srt.py

# 查看CLI帮助
uv run text2srt.py --help

# 快速测试
uv run text2srt.py -t "测试文本" -a 1-1.mp3 -y
```

## 🎯 时间戳问题已解决！

通过改进匹配算法和使用标点分割模式，现在时间戳匹配准确率达到 **100%**，解决了之前段落缺失时间戳的问题。

## 📊 输出格式

### JSON结果格式

```json
{
  "segments": [
    {
      "text": "文本内容",
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

### SRT格式

- **字词级SRT**：每个词一个时间戳，适合精确分析
- **句级SRT**：每句话一个时间戳，适合常规字幕

## ⚙️ 依赖要求

- Python 3.8+
- PyTorch
- qwen-asr
- CUDA支持的GPU以及CPU

## ⚠️ 注意事项

1. **文件编码**：文本文件请使用UTF-8编码
2. **音频格式**：支持常见音频格式（mp3, wav, m4a等）
3. **音频匹配**：音频和文本内容需要匹配
4. **GPU要求**：需要CUDA支持的GPU，CPU也可以
5. **文件命名**：输出文件会自动生成，注意避免重名

## 🎯 应用场景

- **视频字幕制作** - 标点分割模式确保字幕精确对齐
- **语言学习材料** - 完整的字词和句级时间戳辅助学习
- **播客转录** - 精确的分段时间戳便于内容导航
- **语音内容分析** - 详细的字词级时间戳支持精细分析
- **字幕自动生成** - 标点分割避免长段落匹配问题

## 🔧 故障排除

### 常见问题

1. **模型加载失败**

   ```
   [ERROR] 无法加载模型
   ```

   解决：检查CUDA和GPU内存
2. **音频文件不支持**

   ```
   [ERROR] 音频文件不存在
   ```

   解决：检查文件路径和格式
3. **文本读取失败**

   ```
   [ERROR] 读取文件失败
   ```

   解决：确保文本文件使用UTF-8编码
4. **输出目录权限**

   ```
   [ERROR] 无法创建输出目录
   ```

   解决：检查目录权限或选择其他目录

## 🌐 开源项目引用

### 1. 核心引擎

**Qwen3-ASR**: https://github.com/QwenLM/Qwen3-ASR

- 用于音频-文本对齐的强制对齐器
- 支持多语言的精确时间戳提取

### 2. 模型文件

**Qwen3-ForcedAligner-0.6B**: https://huggingface.co/Qwen/Qwen3-ForcedAligner-0.6B

- 高性能的对齐模型，支持日语、中文、英文等多种语言
- 提供准确到词级的精确时间戳

### 3. 相关资源

**Hugging Face Qwen**: https://huggingface.co/Qwen

- 包含Qwen系列的所有模型和资源
- 提供模型下载、配置和使用指南

---

本项目基于Qwen3-ASR和Qwen3-ForcedAligner-0.6B构建，提供高质量的文本时间戳处理解决方案，支持多种语言的精确字幕制作。
