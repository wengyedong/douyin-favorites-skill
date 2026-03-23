---
name: douyin-favorites
description: 用于将抖音视频收藏到本地，包括下载视频，提取文案，总结内容并保存到本地。
required:
  bins: ["ffmpeg", "python", "pip"]
  env: ["FAVORITES_DIR"]
---

# 抖音视频收藏技能

当你收到一个抖音视频收藏请求时，使用该技能将视频收藏到本地。

1. **提取视频链接**：从抖音视频收藏请求中提取视频链接 URL 。
2. **获取收藏目录**：从环境变量中获取收藏目录路径，默认值为 './favorites'。
3. **创建收藏目录**：如果收藏目录不存在，则创建它。
4. **搜藏视频**：调用 douyin-favorites/douyin-favorites.py 脚本将视频收藏到本地，例如（'python douyin-favorites.py --url <URL> --output_dir <FAVORITES_DIR>'）。

### 注意事项：
- 如果链接无效，请礼貌地告知用户检查链接。
- 处理过程可能较慢，请在开始收藏前给用户一个“处理中”的反馈。