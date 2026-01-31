# -*- coding: utf-8 -*-
import json
import os
import re
from datetime import timedelta
from pathlib import Path
from typing import Dict, List, Optional, Union

import torch
from qwen_asr import Qwen3ForcedAligner


class FlexibleTextTimestampProcessor:
    def __init__(self, model_name="Qwen/Qwen3-ForcedAligner-0.6B"):
        """初始化灵活的文本时间戳处理器"""
        self.model = None
        self.model_name = model_name
        self.text_segments = []
        self.word_timestamps = []
        self.matched_segments = []

        # 默认使用标点分割
        self.split_mode = "punctuation"
        self.custom_punctuation = ",.?!、，。！？"  # 自定义分割标点

    def load_model(self):
        """加载ASR模型"""
        if self.model is None:
            print(f"正在加载模型: {self.model_name}")
            self.model = Qwen3ForcedAligner.from_pretrained(
                self.model_name,
                dtype=torch.bfloat16,
                device_map="cuda:0",
            )
            print("模型加载完成")

    def set_custom_punctuation(self, custom_punctuation: str):
        """
        设置自定义分割标点

        Args:
            custom_punctuation: 自定义分割标点符号
        """
        self.custom_punctuation = custom_punctuation
        print(f"使用标点: {self.custom_punctuation}")
        print(f"分割模式: 标点分割")

    def split_text_by_punctuation(self, text: str) -> List[str]:
        """按自定义标点符号分割文本"""
        # 在标点符号后插入"|"
        pattern = f"([{re.escape(self.custom_punctuation)}])"
        text_with_separator = re.sub(pattern, r"\1|", text)

        # 以"|"分割文本
        segments = [
            item.strip() for item in text_with_separator.split("|") if item.strip()
        ]

        self.text_segments = segments
        print(f"标点符号分割完成，共 {len(self.text_segments)} 段")
        print(f"使用标点: {self.custom_punctuation}")
        return self.text_segments

    def split_text(self, text: str) -> List[str]:
        """
        使用标点分割模式分割文本
        """
        return self.split_text_by_punctuation(text)

    def get_word_timestamps(
        self, text: str, audio_path: str, language: str = "Japanese"
    ) -> List[Dict]:
        """获取字词级时间戳"""
        self.load_model()

        print(f"正在处理音频: {audio_path}")
        print(f"文本长度: {len(text)} 字符")

        try:
            results = self.model.align(
                audio=audio_path,
                text=text,
                language=language,
            )

            self.word_timestamps = [
                {
                    "text": item.text,
                    "start_time": item.start_time,
                    "end_time": item.end_time,
                }
                for item in results[0]
            ]

            print(f"字词时间戳获取完成，共 {len(self.word_timestamps)} 个词")
            return self.word_timestamps

        except Exception as e:
            print(f"获取时间戳失败: {e}")
            raise

    def optimized_matching(self) -> List[Dict]:
        """优化的匹配算法"""
        if not self.text_segments or not self.word_timestamps:
            raise ValueError("请先运行文本分割和字词时间戳获取")

        print("正在执行优化匹配...")

        # 构建字词序列
        used_word_indices = set()

        for segment in self.text_segments:
            # 清理目标文本
            target_clean = re.sub(
                f"[{re.escape(self.custom_punctuation)}\\s]", "", segment
            ).lower()

            best_match = None
            best_score = 0
            best_start_idx = 0
            best_end_idx = 0

            # 搜索最佳匹配的字词范围
            for start_idx in range(len(self.word_timestamps)):
                if start_idx in used_word_indices:
                    continue

                for end_idx in range(
                    start_idx + 1, min(start_idx + 30, len(self.word_timestamps) + 1)
                ):
                    # 检查是否与已使用的字词重叠
                    overlap = any(
                        idx in used_word_indices for idx in range(start_idx, end_idx)
                    )
                    if overlap:
                        continue

                    # 构建候选文本
                    candidate_words = self.word_timestamps[start_idx:end_idx]
                    candidate_text = "".join([w["text"] for w in candidate_words])
                    candidate_clean = re.sub(
                        f"[{re.escape(self.custom_punctuation)}\\s]", "", candidate_text
                    ).lower()

                    # 计算相似度
                    if target_clean == candidate_clean:
                        score = 1.0
                    elif target_clean in candidate_clean:
                        score = len(target_clean) / len(candidate_clean)
                    elif candidate_clean in target_clean:
                        score = len(candidate_clean) / len(target_clean)
                    else:
                        # 字符重合度
                        common_chars = set(target_clean) & set(candidate_clean)
                        score = (
                            len(common_chars) / len(target_clean) if target_clean else 0
                        )

                    if score > best_score and score > 0.4:
                        best_score = score
                        best_match = candidate_words
                        best_start_idx = start_idx
                        best_end_idx = end_idx

            if best_match:
                # 记录使用的字词索引
                for idx in range(best_start_idx, best_end_idx):
                    used_word_indices.add(idx)

                start_time = best_match[0]["start_time"]
                end_time = best_match[-1]["end_time"]

                self.matched_segments.append(
                    {
                        "text": segment,
                        "start_time": start_time,
                        "end_time": end_time,
                        "words": best_match,
                        "match_score": best_score,
                        "segment_type": "sentence",
                    }
                )

        # 按时间排序
        self.matched_segments.sort(key=lambda x: x["start_time"])

        print(f"优化匹配完成，共 {len(self.matched_segments)} 个文本段")

        # 显示匹配质量
        high_quality = sum(1 for s in self.matched_segments if s["match_score"] > 0.8)
        print(f"高质量匹配: {high_quality}/{len(self.matched_segments)}")

        return self.matched_segments

    def format_time(self, seconds: float) -> str:
        """将秒数转换为SRT时间格式"""
        td = timedelta(seconds=seconds)
        hours, remainder = divmod(td.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = int((seconds - int(seconds)) * 1000)
        seconds = int(seconds)

        return (
            f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d},{milliseconds:03d}"
        )

    def generate_word_srt(self, output_path: str) -> str:
        """生成字词级SRT字幕文件"""
        print(f"正在生成字词级SRT文件: {output_path}")

        with open(output_path, "w", encoding="utf-8") as f:
            word_index = 1
            for word_info in self.word_timestamps:
                start_time = self.format_time(word_info["start_time"])
                end_time = self.format_time(word_info["end_time"])
                text = word_info["text"]

                if text.strip():
                    f.write(f"{word_index}\n")
                    f.write(f"{start_time} --> {end_time}\n")
                    f.write(f"{text}\n\n")
                    word_index += 1

        print(f"字词级SRT文件生成完成: {output_path}")
        return output_path

    def generate_sentence_srt(self, output_path: str) -> str:
        """生成句级SRT字幕文件"""
        print(f"正在生成句级SRT文件: {output_path}")

        with open(output_path, "w", encoding="utf-8") as f:
            for i, segment in enumerate(self.matched_segments, 1):
                start_time = self.format_time(segment["start_time"])
                end_time = self.format_time(segment["end_time"])
                text = segment["text"]

                if text.strip():
                    f.write(f"{i}\n")
                    f.write(f"{start_time} --> {end_time}\n")
                    f.write(f"{text}\n\n")

        print(f"句级SRT文件生成完成: {output_path}")
        return output_path

    def save_result_json(self, output_path: str = "result.json") -> str:
        """保存结果为JSON文件（格式类似final_matched_timestamps.json）"""
        result_data = {
            "segments": self.matched_segments,
            "statistics": {
                "total_segments": len(self.text_segments),
                "total_words": len(self.word_timestamps),
                "matched_segments": len(self.matched_segments),
                "total_duration": max(w["end_time"] for w in self.word_timestamps)
                if self.word_timestamps
                else 0,
                "split_mode": self.split_mode,
                "punctuation_used": self.custom_punctuation
                if self.split_mode == "punctuation"
                else None,
            },
            "raw_data": {
                "text_segments": self.text_segments,
                "word_timestamps": self.word_timestamps,
            },
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)

        print(f"结果JSON文件保存完成: {output_path}")
        return output_path

    def process(
        self,
        text_input: Union[str, Path],
        audio_path: Union[str, Path],
        language: str = "Japanese",
        json_output: Optional[str] = None,
        word_srt_output: Optional[str] = None,
        sentence_srt_output: Optional[str] = None,
    ) -> Dict:
        """
        完整处理流程，支持文本或文本文件路径输入，按音频文件名命名输出

        Args:
            text_input: 原始文本字符串或文本文件路径
            audio_path: 音频文件路径
            language: 语言（默认Japanese）
            json_output: JSON结果文件路径（可选，默认按音频文件名命名）
            word_srt_output: 字词级SRT文件路径（可选，默认按音频文件名命名）
            sentence_srt_output: 句级SRT文件路径（可选，默认按音频文件名命名）

        Returns:
            包含处理结果的字典
        """
        print("=" * 60)
        print("开始灵活文本时间戳处理（标点分割模式）")
        print("=" * 60)

        try:
            # 1. 加载文本内容
            text = self.load_text(text_input)

            # 2. 生成默认输出文件名（如果未指定）
            if isinstance(audio_path, Path):
                audio_path = str(audio_path)

            if json_output is None:
                json_output = self.get_output_filename(audio_path, ".json")
            if word_srt_output is None:
                word_srt_output = self.get_output_filename(audio_path, "_word.srt")
            if sentence_srt_output is None:
                sentence_srt_output = self.get_output_filename(
                    audio_path, "_sentence.srt"
                )

            # 3. 文本分割
            self.split_text(text)

            # 4. 获取字词时间戳
            self.get_word_timestamps(text, audio_path, language)

            # 5. 优化匹配
            self.optimized_matching()

            # 6. 保存JSON结果
            self.save_result_json(json_output)

            # 7. 生成字词级SRT
            self.generate_word_srt(word_srt_output)

            # 8. 生成句级SRT
            self.generate_sentence_srt(sentence_srt_output)

            print("=" * 60)
            print("灵活处理完成！")
            print(f"JSON文件: {json_output}")
            print(f"字词级SRT: {word_srt_output}")
            print(f"句级SRT: {sentence_srt_output}")
            print("=" * 60)

            return {
                "segments": self.matched_segments,
                "statistics": {
                    "total_segments": len(self.text_segments),
                    "total_words": len(self.word_timestamps),
                    "matched_segments": len(self.matched_segments),
                },
                "output_files": {
                    "json": json_output,
                    "word_srt": word_srt_output,
                    "sentence_srt": sentence_srt_output,
                },
            }

        except Exception as e:
            print(f"处理失败: {e}")
            raise

    def load_text(self, text_input: Union[str, Path]) -> str:
        """加载文本内容，支持直接文本或文件路径"""
        if isinstance(text_input, Path):
            text_input = str(text_input)

        # 检查是否为文件路径
        if os.path.isfile(text_input):
            print(f"正在读取文本文件: {text_input}")
            try:
                with open(text_input, "r", encoding="utf-8") as f:
                    text = f.read()
                print(f"文本文件读取完成，长度: {len(text)} 字符")
                return text
            except Exception as e:
                print(f"读取文本文件失败: {e}")
                raise
        else:
            # 直接输入文本
            print(f"使用直接输入文本，长度: {len(text_input)} 字符")
            return text_input

    def get_output_filename(self, audio_path: Union[str, Path], suffix: str) -> str:
        """根据音频文件路径生成输出文件名"""
        if isinstance(audio_path, Path):
            audio_path = str(audio_path)

        # 获取音频文件名（不含扩展名）
        audio_filename = Path(audio_path).stem
        return f"{audio_filename}{suffix}"


def main():
    """演示使用示例"""

    # 示例文本
    text = """世界で一番有名な富士山の絵、葛飾北斉。1998年に、アメリカの雑誌《ライフ》が、この千年の間の世界のすごい人、100人を選びました。その中に、一人の日本人がいます。誰だと思いますか？漫画やアニメの作者でしょうか。いいえ、《ライフ》が選んだのは葛飾北斉でした。北斉は江戸時代の浮世絵の画家です。北斉の名前は知らないかもしれませんが、たぶん皆さんも、大きい青い波の間に富士山が見える浮世絵を見たことがあるでしょう。日本語では、この浮世絵のを神奈川沖浪裏と言いますが、英語では、ザーグレートウェーブと言います。そして、これは北斉の浮世絵です。"""
    temp_text_file = "temp.txt"
    # 音频文件路径
    audio_path = "1-1.mp3"

    try:
        # 示例1：标点分割（默认）
        print("=== 示例1：标点分割（默认） ===")
        processor = FlexibleTextTimestampProcessor()
        result1 = processor.process(text_input=text, audio_path=audio_path)

        # 示例2：从文本文件读取
        print("\n=== 示例2：从文本文件读取 ===")

        with open(temp_text_file, "w", encoding="utf-8") as f:
            f.write(text)

        processor2 = FlexibleTextTimestampProcessor()
        result2 = processor2.process(text_input=temp_text_file, audio_path=audio_path)

        # 示例3：自定义文件名
        print("\n=== 示例3：自定义文件名 ===")
        processor3 = FlexibleTextTimestampProcessor()
        result3 = processor3.process(
            text_input=text,
            audio_path=audio_path,
            json_output="my_result.json",
            word_srt_output="my_word.srt",
            sentence_srt_output="my_sentence.srt",
        )
        # 显示结果
        print("\n=== 结果对比 ===")
        print(f"标点分割: {result1['statistics']['total_segments']} 段")
        print(f"文件读取: {result2['statistics']['total_segments']} 段")
        print(f"自定义输出: {result3['statistics']['total_segments']} 段")
        print(f"输出文件: {result1['output_files']}")

    except Exception as e:
        print(f"处理失败: {e}")


if __name__ == "__main__":
    main()
