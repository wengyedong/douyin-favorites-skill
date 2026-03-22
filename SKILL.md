---
name: douyin-favorites
description: 用于将抖音视频收藏到本地，包括下载视频，提取文案，总结内容并保存到本地。
required:
  bins: ["ffmpeg", "python", "pip"]
---

# 抖音视频收藏技能

当你收到一个抖音视频收藏请求时，使用该技能将视频收藏到本地。

1. **下载视频**：调用 douyin-downloader/douyin-downloader.py 脚本将视频下载到本地，例如（'python douyin-downloader.py --url <URL>'）。
2. **提取文案**：调用 video-script-extractor/transcribe_tool.py 脚本从视频中提取文案，例如（'python transcribe_tool.py'）。
3. **总结内容**：调用 douyin-summarizer/douyin-summarizer.py 脚本对提取的文案进行总结，例如（'douyin-summarizer.py --text <TEXT>'）。
4. **保存到本地**：将总结的内容保存到本地文件中，例如（'echo "总结内容" > <OUTPUT_FILE>'）。