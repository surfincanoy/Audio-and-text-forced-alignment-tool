import json
import os
import re
import subprocess
from datetime import timedelta
from pathlib import Path

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
        self.custom_punctuation = "、。！？"

    def load_model(self):
        """加载ASR模型"""
        if self.model is None:
            print(f"正在加载模型: {self.model_name}")
            self.model = Qwen3ForcedAligner.from_pretrained(
                self.model_name,
                dtype=torch.bfloat16,
                device_map="cpu" if not torch.cuda.is_available() else "cuda:0",
            )
            print("模型加载完成")

    def set_custom_punctuation(self, custom_punctuation: str):
        """设置自定义分割标点"""
        self.custom_punctuation = custom_punctuation
        print(f"使用标点: {self.custom_punctuation}")
        print(f"分割模式: 标点分割")

    def split_text_by_punctuation(self, text: str):
        """按自定义标点符号分割文本"""
        pattern = f"([{re.escape(self.custom_punctuation)}])"
        text_with_separator = re.sub(pattern, r"\1|", text)
        segments = [
            item.strip() for item in text_with_separator.split("|") if item.strip()
        ]

        self.text_segments = segments
        print(f"标点符号分割完成，共 {len(self.text_segments)} 段")
        print(f"使用标点: {self.custom_punctuation}")
        return self.text_segments

    def split_text(self, text: str):
        """使用标点分割模式分割文本"""
        return self.split_text_by_punctuation(text)

    def get_word_timestamps(
        self, text: str, audio_path: str, language: str = "Japanese"
    ):
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

    def optimized_matching(self):
        """优化的匹配算法"""
        if not self.text_segments or not self.word_timestamps:
            raise ValueError("请先运行文本分割和字词时间戳获取")

        print("正在执行优化匹配...")

        used_word_indices = set()

        for segment in self.text_segments:
            target_clean = re.sub(
                f"[{re.escape(self.custom_punctuation)}\\s]", "", segment
            ).lower()

            best_match = None
            best_score = 0
            best_start_idx = 0
            best_end_idx = 0

            for start_idx in range(len(self.word_timestamps)):
                if start_idx in used_word_indices:
                    continue

                for end_idx in range(
                    start_idx + 1, min(start_idx + 30, len(self.word_timestamps) + 1)
                ):
                    overlap = any(
                        idx in used_word_indices for idx in range(start_idx, end_idx)
                    )
                    if overlap:
                        continue

                    candidate_words = self.word_timestamps[start_idx:end_idx]
                    candidate_text = "".join([w["text"] for w in candidate_words])
                    candidate_clean = re.sub(
                        f"[{re.escape(self.custom_punctuation)}\\s]", "", candidate_text
                    ).lower()

                    if target_clean == candidate_clean:
                        score = 1.0
                    elif target_clean in candidate_clean:
                        score = len(target_clean) / len(candidate_clean)
                    elif candidate_clean in target_clean:
                        score = len(candidate_clean) / len(target_clean)
                    else:
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

        self.matched_segments.sort(key=lambda x: x["start_time"])

        print(f"优化匹配完成，共 {len(self.matched_segments)} 个文本段")
        high_quality = sum(1 for s in self.matched_segments if s["match_score"] > 0.8)
        print(f"高质量匹配: {high_quality}/{len(self.matched_segments)}")

        return self.matched_segments

    def format_time(self, seconds: float):
        """将秒数转换为SRT时间格式"""
        td = timedelta(seconds=seconds)
        hours, remainder = divmod(td.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = int((seconds - int(seconds)) * 1000)
        seconds = int(seconds)

        return (
            f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d},{milliseconds:03d}"
        )

    def generate_word_srt(self, output_path: str):
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

    def generate_sentence_srt(self, output_path: str):
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

    def save_result_json(self, output_path: str = "result.json"):
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

    def get_output_filename(self, audio_path, suffix: str):
        """根据音频文件路径生成输出文件名"""
        audio_filename = Path(audio_path).stem
        return f"{audio_filename}{suffix}"

    def load_text(self, text_input):
        """加载文本内容，支持直接文本或文件路径"""
        if isinstance(text_input, Path):
            text_input = str(text_input)

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
            print(f"使用直接输入文本，长度: {len(text_input)} 字符")
            return text_input

    def process_video_file(self, video_path):
        """处理视频文件（先转换为音频）"""
        video_path = str(video_path)

        if not os.path.isfile(video_path):
            print(f"[ERROR] 视频文件不存在: {video_path}")
            return None

        video_ext = Path(video_path).suffix.lower()
        print(f"[INFO] 检测到视频文件: {video_path}")

        try:
            video_path_no_ext = (
                video_path[: -len(video_ext)] if video_ext else video_path
            )
            temp_audio_path = f"{video_path_no_ext}_temp_audio.mp3"

            print(f"[INFO] 开始转换视频为音频: {video_path} -> {temp_audio_path}")

            if video_ext in [".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm"]:
                cmd = [
                    "ffmpeg",
                    "-i",
                    video_path,
                    "-vn",
                    "-acodec",
                    "mp3",
                    "-ar",
                    "44100",
                    "-ab",
                    "128k",
                    "-y",
                    temp_audio_path,
                ]

                print(f"[INFO] 执行转换命令: {' '.join(cmd)}")

                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                )

                if result.returncode == 0:
                    print(f"[INFO] 视频转换完成: {temp_audio_path}")

                    try:
                        os.remove(video_path)
                        print(f"[INFO] 已删除原始视频文件: {video_path}")
                    except Exception as e:
                        print(f"[WARNING] 删除视频文件失败: {e}")

                    return temp_audio_path
                else:
                    print(f"[ERROR] 视频转换失败:")
                    print(result.stderr)
                    return None
            else:
                print(f"[ERROR] 不支持的视频格式: {video_ext}")
                print(
                    f"[INFO] 支持的格式: {', '.join(['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm'])}"
                )
                return None

        except Exception as e:
            print(f"[ERROR] 视频转换失败: {e}")
            return None

    def process_media_file(self, media_path, text_input, **kwargs):
        """处理媒体文件（自动检测视频或音频）"""
        media_path = str(media_path)
        media_ext = Path(media_path).suffix.lower()

        if not os.path.isfile(media_path):
            print(f"[ERROR] 媒体文件不存在: {media_path}")
            return None

        video_extensions = {".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm"}
        audio_extensions = {".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac"}

        if media_ext in video_extensions:
            print(f"[INFO] 检测到视频文件: {media_path}")
            return self.process_video_file(media_path)
        elif media_ext in audio_extensions:
            print(f"[INFO] 检测到音频文件: {media_path}")
            # 直接使用音频文件处理
            media_stem = Path(media_path).stem
            json_output = kwargs.get("json_output", f"{media_stem}.json")
            word_srt_output = kwargs.get("word_srt_output", f"{media_stem}_word.srt")
            sentence_srt_output = kwargs.get(
                "sentence_srt_output", f"{media_stem}_sentence.srt"
            )

            return self.process(
                text_input=text_input,
                audio_path=media_path,
                json_output=json_output,
                word_srt_output=word_srt_output,
                sentence_srt_output=sentence_srt_output,
                **{
                    k: v
                    for k, v in kwargs.items()
                    if k
                    not in ["json_output", "word_srt_output", "sentence_srt_output"]
                },
            )
        else:
            print(f"[ERROR] 不支持的媒体格式: {media_ext}")
            print(f"[INFO] 支持的视频格式: {', '.join(video_extensions)}")
            print(f"[INFO] 支持的音频格式: {', '.join(audio_extensions)}")
            return None

    def process(
        self,
        text_input,
        audio_path,
        language="Japanese",
        json_output=None,
        word_srt_output=None,
        sentence_srt_output=None,
    ):
        """完整处理流程"""
        print("=" * 60)
        print("开始灵活文本时间戳处理")
        print("=" * 60)

        try:
            text = self.load_text(text_input)

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

            self.split_text(text)
            self.get_word_timestamps(text, audio_path, language)
            self.optimized_matching()
            self.save_result_json(json_output)
            self.generate_word_srt(word_srt_output)
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


def main():
    """演示使用示例:输入音视频文件，文本字符或者文本文件"""
    text = """世界で一番有名な富士山の絵、葛飾北斉。1998年にアメリカの雑誌《ライフ》がこの千年の間の世界のすごい人100人を選びました。その中に一人の日本人がいます。誰だと思いますか？漫画やアニメの作者でしょうか。いいえ、《ライフ》が選んだのは葛飾北斉でした。北斉は江戸時代の浮世絵の画家です。"""

    try:
        processor = FlexibleTextTimestampProcessor()

        print("=== 示例1：音频文件处理 ===")
        audio_path = "1-1.mp3"
        result1 = processor.process(text_input=text, audio_path=audio_path)

        print("\n=== 示例2：视频文件处理（如果存在） ===")
        video_path = "sample_video.mp4"  # 示例视频文件
        if os.path.exists(video_path):
            result2 = processor.process_media_file(
                media_path=video_path,
                text_input=text,
            )
            if result2:
                print("视频处理成功！")
        else:
            print(f"示例视频文件不存在: {video_path}")

    except Exception as e:
        print(f"处理失败: {e}")


if __name__ == "__main__":
    main()
