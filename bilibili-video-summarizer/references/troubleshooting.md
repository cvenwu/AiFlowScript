# 排障

## Cookie 相关

- `not_set`：环境变量 `BILIBILI_COOKIE` 未设置。从浏览器 DevTools > Application > Cookies 复制 `bilibili.com` 域下的完整 cookie 字符串（至少含 `SESSDATA`）。
- `invalid`：cookie 已失效或格式不对。重新登录 bilibili.com 复制新 cookie。

## yt-dlp / ffmpeg 缺失

- `未检测到 yt-dlp`：`pip install yt-dlp`
- `未检测到 ffmpeg`：macOS `brew install ffmpeg`

## 视频无字幕

自动降级为 Whisper 本地转录。若报 `未安装 openai-whisper`：

```bash
pip install openai-whisper
```

首次运行会下载模型（几百 MB）。

## 关键帧过少

场景检测抽到 <3 张时，脚本自动降级为均匀抽帧（8~12 张）。若均匀抽帧仍失败，检查视频文件是否成功下载。

## 链接解析失败

只接受包含 `BVxxxxxxxxxx` 的完整链接。若你有短链（如 `b23.tv/xxx`），先在浏览器打开跳转到完整链接，再复制回来。
