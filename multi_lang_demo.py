#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多语言文本时间戳处理示例（编码修复版）
"""

import locale
import subprocess
import sys
from pathlib import Path

# 设置控制台编码
try:
    sys.stdout.reconfigure(encoding="utf-8")
    if sys.stderr:
        sys.stderr.reconfigure(encoding="utf-8")
except:
    pass


def process_text(text, audio_file, language_code, language_name):
    """处理指定语言的文本"""
    try:
        print(f"=== {language_name} 示例 ===")
        print(f"文本: {text}")
        print(f"音频: {audio_file}")
        print(f"语言: {language_code}")

        # 创建临时文本文件
        temp_file = f"temp_{language_code}.txt"
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(text)

        # 执行处理命令
        cmd = [
            "uv",
            "run",
            "text2srt.py",
            "-t",
            temp_file,
            "-a",
            audio_file,
            "-l",
            language_code,
            "-p",
            ",.?!、。！？",
            "-y",
        ]

        result = subprocess.run(
            cmd, capture_output=True, text=True, encoding="utf-8", errors="replace"
        )

        # 清理临时文件
        import os

        os.remove(temp_file)

        if result.returncode == 0:
            print(f"✓ {language_name} 处理成功！")
            return True
        else:
            print(f"✗ {language_name} 处理失败:")
            print(result.stderr)
            return False

    except Exception as e:
        print(f"✗ {language_name} 处理出错: {str(e)}")
        return False

    print("-" * 50)
    return True


def main():
    """主函数"""
    print("=" * 50)
    print("多语言文本时间戳处理示例")
    print("=" * 50)

    # 示例文本
    examples = [
        {
            "name": "日本語",
            "text": "世界で一番有名な富士山の絵、葛飾北斉。",
            "audio": "1-1.mp3",
            "code": "Japanese",
        },
        {
            "name": "中文",
            "text": "这是第一句话。这是第二句话！这是第三句话？",
            "audio": "1-1.mp3",
            "code": "Chinese",
        },
        {
            "name": "English",
            "text": "This is the first sentence. This is the second sentence! Is this the third question?",
            "audio": "1-1.mp3",
            "code": "English",
        },
    ]

    success_count = 0

    for example in examples:
        if process_text(
            example["text"], example["audio"], example["code"], example["name"]
        ):
            success_count += 1

    print("\n" + "=" * 50)
    print(f"处理完成！成功: {success_count}/{len(examples)}")
    print("=" * 50)

    # 显示输出文件
    audio_name = Path("1-1.mp3").stem
    output_files = list(Path(".").glob(f"{audio_name}*"))

    if output_files:
        print("\n📁 生成的输出文件:")
        for file in sorted(output_files):
            print(f"   📄 {file}")
    else:
        print("\n⚠️ 未找到输出文件")

    print("\n💡 使用方法:")
    print("1. 直接使用:")
    print("   uv run text2srt.py -t 'your text' -a audio.mp3 -l Japanese -y")
    print("2. 从文件读取:")
    print("   uv run text2srt.py -t text.txt -a audio.mp3 -l Japanese -y")
    print("3. 自定义标点:")
    print(
        "   uv run text2srt.py -t text.txt -a audio.mp3 -l Japanese -p ',.!?。！？' -y"
    )


if __name__ == "__main__":
    main()
