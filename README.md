# 抖音视频收藏工具

一个集成了抖音视频下载和文案提取功能的综合工具，帮助用户快速收藏和整理抖音视频内容。

## 项目结构

```
douyin-favorites-skill/
├── douyin-downloader/     # 抖音视频下载子模块
├── video-script-extractor/ # 视频文案提取子模块
├── douyin-favorites.py     # 主脚本
├── .gitignore
├── .gitmodules
├── SKILL.md
└── README.md              # 项目说明文档
```

## 功能特性

- 📥 **视频下载**：支持从抖音链接下载视频，自动解析短链接，优先选择高清版本
- 📝 **文案提取**：自动将视频中的语音转换为文字，生成结构化的转录文件
- 📁 **智能组织**：按视频 ID 自动创建输出目录，避免文件名冲突
- 📊 **信息保存**：生成包含视频标题、时长、ID 等信息的 JSON 文件
- 🎯 **多格式输出**：同时生成 JSON 和 Markdown 格式的转录结果
- ⚡ **硬件加速**：自动检测 CUDA 可用性，优先使用 GPU 加速语音识别
- 🔄 **自动清理**：完成后自动清理临时文件，保持目录整洁

## 安装指南

### 1. 克隆项目

```bash
git clone https://github.com/wengyedong/douyin-favorites-skill.git
cd douyin-favorites-skill

# 初始化子模块
git submodule update --init --recursive
```

### 2. 安装依赖

#### 方法一：直接安装主项目依赖（推荐）

主项目已提供合并后的 `requirements.txt` 文件，包含所有子模块的依赖：

```bash
pip install -r requirements.txt

# 或使用国内源加速
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 方法二：单独安装子模块依赖

```bash
# 安装抖音下载器依赖
cd douyin-downloader
pip install -r requirements.txt
cd ..

# 安装视频文案提取器依赖
cd video-script-extractor
pip install -r requirements.txt
cd ..
```

#### 安装系统依赖

**ffmpeg**（视频文案提取需要）：

##### Windows 安装步骤

1. 访问 [ffmpeg 官网](https://ffmpeg.org/download.html) 下载 Windows 版本
2. 选择 "Windows builds from gyan.dev" 或 "Windows builds from BtbN"
3. 下载最新的静态版本（static build）
4. 解压下载的压缩包到任意目录，例如 `C:\ffmpeg`
5. 将 `C:\ffmpeg\bin` 目录添加到系统环境变量 `PATH`：
   - 右键点击 "此电脑" → "属性" → "高级系统设置" → "环境变量"
   - 在 "系统变量" 中找到 "Path"，点击 "编辑"
   - 点击 "新建"，输入 `C:\ffmpeg\bin`（根据实际解压路径调整）
   - 点击 "确定" 保存所有更改
6. 验证安装：打开命令提示符，输入 `ffmpeg -version`，如果显示版本信息则安装成功

##### Linux 安装步骤

**Ubuntu/Debian**：
```bash
apt update && apt install ffmpeg -y
```

**CentOS/RHEL**：
```bash
yum install epel-release -y
yum install ffmpeg ffmpeg-devel -y
```

**验证安装**：
```bash
ffmpeg -version
```

##### macOS 安装步骤

**使用 Homebrew**：
```bash
brew install ffmpeg
```

**验证安装**：
```bash
ffmpeg -version
```

## 使用方法

### 基本用法

```bash
python douyin-favorites.py <抖音视频链接>
```

### 指定输出目录

```bash
python douyin-favorites.py <抖音视频链接> --output-dir <输出目录路径>
```

## 示例

### 下载并提取抖音视频

```bash
# 基本用法
python douyin-favorites.py https://v.douyin.com/KqkNll9Dn3g/

# 指定输出目录
python douyin-favorites.py https://v.douyin.com/KqkNll9Dn3g/ --output-dir D:\DouyinFavorites
```

## 输出文件

执行完成后，会在输出目录中生成以下文件结构：

```
output/
└── <视频ID>/            # 按视频ID命名的目录
    ├── <视频ID>.mp4     # 下载的视频文件
    ├── <视频ID>_info.json  # 视频信息文件
    ├── <视频ID>.json    # 文案转录JSON文件
    └── <视频ID>.md      # 文案转录Markdown文件
```

### 视频信息文件 (`<视频ID>_info.json`)

```json
{
  "title": "视频标题",
  "duration": "视频时长",
  "tiktok_id": "视频ID",
  "original_url": "原始抖音链接"
}
```

### 文案转录文件

#### JSON 格式 (`<视频ID>.json`)

```json
{
  "video_path": "视频文件路径",
  "duration": 视频时长,
  "language": "识别语言",
  "segments": [
    {
      "start": 开始时间,
      "end": 结束时间,
      "text": "转录文本"
    }
  ]
}
```

#### Markdown 格式 (`<视频ID>.md`)

```markdown
# 视频转录结果

**视频路径**: 视频文件路径
**时长**: 视频时长
**识别语言**: 识别语言

## 转录内容

### [00:00 → 00:05]
转录文本
```

## 依赖项

### Python 依赖

- **douyin-downloader**：
  - Python 3.6+
  - requests
  - beautifulsoup4
  - tqdm

- **video-script-extractor**：
  - Python 3.7+
  - faster-whisper
  - tqdm
  - torch
  - ffmpeg（系统依赖）

### 系统依赖

- **ffmpeg**：用于音频提取

## 系统要求

- **CPU 模式**：任何现代 CPU 均可运行
- **GPU 模式**：需要 NVIDIA 显卡和 CUDA 支持（可选，用于加速语音识别）

## 注意事项

1. **首次运行**：首次运行时，video-script-extractor 会下载模型文件（约 1.5GB），请确保网络连接正常
2. **网络要求**：视频下载速度取决于网络状况
3. **视频限制**：部分视频可能因版权或其他原因无法下载
4. **硬件要求**：
   - GPU 模式：推荐 NVIDIA GTX 1060 或更高
   - CPU 模式：可能会较慢，适合短视频
5. **使用规范**：本工具仅用于个人学习和研究，请勿用于商业用途
6. **平台规范**：请遵守抖音平台的相关规定

## 故障排除

### 常见错误

1. **网络请求错误**：可能是网络连接问题，程序会自动重试
2. **未找到视频数据**：可能是链接无效或视频已被删除
3. **ffmpeg 未安装**：请按照安装指南安装 ffmpeg 并添加到 PATH
4. **依赖项缺失**：运行 `pip install -r requirements.txt` 安装缺失的依赖
5. **CUDA 不可用**：将自动切换到 CPU 模式，识别速度会变慢
6. **模型下载失败**：检查网络连接，重新运行命令

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！

## 项目链接

- **主项目**：https://github.com/wengyedong/douyin-favorites-skill
- **抖音下载器**：https://github.com/wengyedong/douyin-downloader
- **视频文案提取器**：https://github.com/wengyedong/video-script-extractor