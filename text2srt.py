#!/usr/bin/env python3
"""
命令行版本的媒体文件时间戳处理工具
"""

import argparse
import sys
from pathlib import Path

from flexible_processor import FlexibleTextTimestampProcessor


def main():
    parser = argparse.ArgumentParser(description="媒体文件时间戳处理工具")

    parser.add_argument("-t", "--text", help="文本内容或文本文件路径")
    parser.add_argument("-a", "--audio", help="音频文件路径")
    parser.add_argument("-v", "--video", help="视频文件路径（会自动转换为音频）")
    parser.add_argument(
        "-l", "--language", default="Japanese", help="语言 (默认: Japanese)"
    )

    args = parser.parse_args()

    # 参数验证
    if not args.text:
        print("请提供文本内容或文件路径 (-t)")
        parser.print_help()
        sys.exit(1)

    if not args.audio and not args.video:
        print("请提供音频文件路径 (-a) 或视频文件路径 (-v)")
        parser.print_help()
        sys.exit(1)

    if args.audio and args.video:
        print("不能同时指定音频和视频文件")
        sys.exit(1)

    # 创建处理器
    processor = FlexibleTextTimestampProcessor()

    try:
        print("开始处理...")

        if args.video:
            # 处理视频文件
            if not Path(args.video).exists():
                print(f"视频文件不存在: {args.video}")
                sys.exit(1)

            print(f"检测到视频文件: {args.video}")
            result = processor.process_media_file(
                media_path=args.video, text_input=args.text
            )
        else:
            # 处理音频文件
            if not Path(args.audio).exists():
                print(f"音频文件不存在: {args.audio}")
                sys.exit(1)

            result = processor.process(
                text_input=args.text, audio_path=args.audio, language=args.language
            )

        if result:
            output_files = result["output_files"]
            stats = result["statistics"]

            print("\n✅ 处理成功!")
            print(f"生成文件: {len(output_files)} 个")
            for file_type, file_path in output_files.items():
                print(f"  - {file_type}: {file_path}")

            print(f"\n统计信息:")
            print(f"  - 段落数: {stats['total_segments']}")
            print(f"  - 词数: {stats['total_words']}")
            print(f"  - 匹配率: {stats['matched_segments']}/{stats['total_segments']}")
        else:
            print("❌ 处理失败")

    except Exception as e:
        print(f"❌ 错误: {e}")


if __name__ == "__main__":
    main()
