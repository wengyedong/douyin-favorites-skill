#!/usr/bin/env python3
import os
import sys
import argparse
import json
from pathlib import Path

# 添加子模块路径到系统路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'douyin-downloader'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'video-script-extractor'))

# 导入子模块中的函数
try:
    from douyin_downloader import download_douyin_video
except ImportError:
    print("Error: Could not import douyin_downloader module")
    sys.exit(1)

try:
    from video_extractor import video_extractor
except ImportError:
    print("Error: Could not import video_extractor module")
    sys.exit(1)

# 实现命令行参数解析
def parse_arguments():
    parser = argparse.ArgumentParser(description='抖音视频收藏工具')
    parser.add_argument('url', help='抖音视频链接')
    return parser.parse_args()

# 确保 temp 目录存在
def ensure_temp_dir():
    temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    return temp_dir

# 检索最新的视频文件和 JSON 信息文件
def find_latest_files(temp_dir):
    video_files = []
    json_files = []
    
    # 遍历 temp 目录及其子目录
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.mp4'):
                video_files.append((file_path, os.path.getmtime(file_path)))
            elif file.endswith('_info.json'):
                json_files.append((file_path, os.path.getmtime(file_path)))
    
    # 按修改时间排序，获取最新的文件
    if not video_files:
        print("未找到视频文件")
        return None, None
    
    # 按修改时间排序，获取最新的视频文件
    video_files.sort(key=lambda x: x[1], reverse=True)
    latest_video = video_files[0][0]
    
    # 查找对应的 JSON 文件
    latest_json = None
    if json_files:
        json_files.sort(key=lambda x: x[1], reverse=True)
        latest_json = json_files[0][0]
    
    return latest_video, latest_json

if __name__ == '__main__':
    args = parse_arguments()
    print(f"抖音视频链接: {args.url}")
    
    # 确保 temp 目录存在
    temp_dir = ensure_temp_dir()
    print(f"临时目录: {temp_dir}")
    
    # 下载视频
    print("开始下载视频...")
    try:
        success = download_douyin_video(args.url, temp_dir)
        if not success:
            print("下载失败: 未找到视频数据")
            sys.exit(1)
        print("视频下载完成")
    except Exception as e:
        print(f"下载失败: {e}")
        sys.exit(1)
    
    # 检索最新的视频文件和 JSON 信息文件
    print("检索视频文件...")
    video_file, json_file = find_latest_files(temp_dir)
    if not video_file:
        print("未找到视频文件")
        sys.exit(1)
    print(f"找到视频文件: {video_file}")
    if json_file:
        print(f"找到 JSON 信息文件: {json_file}")
    
    # 提取视频文案
    print("开始提取视频文案...")
    try:
        video_extractor(video_file, temp_dir)
        print("视频文案提取完成")
    except Exception as e:
        print(f"文案提取失败: {e}")
        sys.exit(1)