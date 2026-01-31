#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文本时间戳处理CLI工具（标点分割版）
"""

import argparse
import os
import sys
from pathlib import Path

from flexible_processor import FlexibleTextTimestampProcessor


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="文本时间戳处理CLI工具（标点分割版）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # 必需参数
    parser.add_argument("-t", "--text", required=True, help="文本内容或文本文件路径")
    parser.add_argument("-a", "--audio", required=True, help="音频文件路径")

    # 可选参数
    parser.add_argument("-o", "--output", help="输出目录路径（默认：音频文件所在目录）")
    parser.add_argument(
        "-p", "--punctuation", default="，?.,!、。！？", help="自定义分割标点"
    )
    parser.add_argument("-l", "--language", default="Japanese", help="音频语言")
    parser.add_argument("-y", "--yes", action="store_true", help="跳过确认，直接处理")

    args = parser.parse_args()

    print("=" * 60)
    print("文本时间戳处理CLI工具（标点分割版）")
    print("=" * 60)

    # 检查音频文件
    if not os.path.isfile(args.audio):
        print(f"[ERROR] 音频文件不存在: {args.audio}")
        sys.exit(1)

    # 确定输出目录
    if args.output:
        output_dir = args.output
    else:
        output_dir = str(Path(args.audio).parent)

    # 创建输出目录
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    print(f"[INFO] 输出目录: {output_dir}")

    # 获取文本内容
    if os.path.isfile(args.text):
        print(f"[INFO] 从文件读取文本: {args.text}")
        try:
            with open(args.text, "r", encoding="utf-8") as f:
                text = f.read()
            print(f"[INFO] 文本读取完成，长度: {len(text)} 字符")
        except Exception as e:
            print(f"[ERROR] 读取文件失败: {e}")
            sys.exit(1)
    else:
        text = args.text
        print(f"[INFO] 使用直接输入文本，长度: {len(text)} 字符")

    # 生成输出文件路径
    audio_name = Path(args.audio).stem
    json_output = os.path.join(output_dir, f"{audio_name}.json")
    word_srt_output = os.path.join(output_dir, f"{audio_name}_word.srt")
    sentence_srt_output = os.path.join(output_dir, f"{audio_name}_sentence.srt")

    print(f"[INFO] 预期输出文件:")
    print(f"   JSON: {json_output}")
    print(f"   字词级SRT: {word_srt_output}")
    print(f"   句级SRT: {sentence_srt_output}")
    print(f"[INFO] 分割模式: 标点分割")
    print(f"[INFO] 使用标点: {args.punctuation}")
    print(f"[INFO] 音频语言: {args.language}")
    print()

    # 确认继续
    if not args.yes:
        response = input("是否继续处理？(Y/n): ").strip().lower()
        if response and response != "y":
            print("[INFO] 用户取消操作")
            sys.exit(0)

    try:
        print("[INFO] 开始处理...")

        # 创建处理器
        processor = FlexibleTextTimestampProcessor()

        # 设置分割标点
        processor.set_custom_punctuation(args.punctuation)

        # 执行处理
        result = processor.process(
            text_input=text,
            audio_path=args.audio,
            language=args.language,
            json_output=json_output,
            word_srt_output=word_srt_output,
            sentence_srt_output=sentence_srt_output,
        )

        print()
        print("=" * 60)
        print("[SUCCESS] 处理完成！")
        print("=" * 60)
        print(f"[STATISTICS] 处理统计:")
        print(f"   文本段数: {result['statistics']['total_segments']}")
        print(f"   字词数量: {result['statistics']['total_words']}")
        print(f"   匹配段数: {result['statistics']['matched_segments']}")
        print()
        print(f"[OUTPUT] 输出文件:")
        print(f"   {json_output}")
        print(f"   {word_srt_output}")
        print(f"   {sentence_srt_output}")

    except KeyboardInterrupt:
        print("\n[ERROR] 用户中断处理")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] 处理失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
