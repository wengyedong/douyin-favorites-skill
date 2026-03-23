#!/usr/bin/env python3
import os
import sys
import argparse
import json
from pathlib import Path
import shutil
from datetime import datetime



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
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="抖音视频收藏工具")
    parser.add_argument("url", help="抖音视频链接")
    parser.add_argument("--output-dir", dest="output_dir", help="指定输出目录路径", default=os.path.join(os.path.dirname(__file__), 'output'))
    args = parser.parse_args()

    print(f"抖音视频链接: {args.url}")
    print(f"输出目录: {args.output_dir}")
    
    # 清除临时目录（如果存在），并创建新的 temp 目录
    temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
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
    
    # 解析 JSON 信息文件
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        title = data.get('title', '无标题')
        print(f"视频标题: {title}")
        duration = data.get('duration', '无时长')
        print(f"视频时长: {duration}")
        tiktok_id = data.get('tiktok_id', '无抖音 ID')
        print(f"抖音 ID: {tiktok_id}")
        original_url = data.get('original_url', '无原始链接')
        print(f"原始链接: {original_url}")

    video_dir = os.path.dirname(video_file)
    output_dir = os.path.join(args.output_dir, tiktok_id)

    # 提取视频文案
    print("开始提取视频文案...")
    try:
        video_extractor(video_file, video_dir)
        print("视频文案提取完成")
    except Exception as e:
        print(f"文案提取失败: {e}")
        sys.exit(1)

    # 拷贝结果（video_dir）到输出目录，如果目录已存在则提示用户，并增加时间戳
    if os.path.exists(output_dir):
        print(f"输出目录已存在: {output_dir}")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_dir = os.path.join(args.output_dir, f"{tiktok_id}_{timestamp}")
        print(f"调整输出目录为: {output_dir}")
    print(f"开始拷贝结果到 {output_dir}...")
    shutil.copytree(video_dir, output_dir)
    print("结果拷贝完成")
    print(f"结果已保存到: {output_dir}")

    # 清除临时目录
    try:
        print(f"开始清除临时目录 {temp_dir}...")
        shutil.rmtree(temp_dir)
        print("临时目录已清除")
    except Exception as e:
        print(f"清除临时目录失败: {e}")
        sys.exit(1)
