# 🎨 Pixel Art Generator (CPU/GPU Simulation)

## 📖 Project Overview (项目简介)
**Pixel Art Generator** is a web-based application that converts uploaded images into retro-style pixel art. 
**像素画生成器** 是一个 Web 应用程序，可以将上传的图像转换为复古风格的像素画。

The core purpose of this project is to demonstrate the **performance difference between Serial Processing (CPU) and Vectorized Processing (GPU simulation)**.
本项目的核心目的是演示 **串行处理 (CPU) 与 向量化处理 (GPU 模拟)** 之间的性能差异。

---

## 🚀 Features (功能特性)
- **Web Interface**: Clean UI for uploading images and viewing results instantly.
- **Dual Modes**:
  - **CPU Mode**: Simulates traditional loop-based image processing (Slow).
  - **GPU Mode**: Simulates parallel processing using NumPy vectorization (Fast).
- **Adjustable Detail**: Choose pixel block sizes (8px, 16px, 32px).

---

## 🛠️ Installation & Setup (安装与运行)

### 1. Prerequisites (环境要求)
- Python 3.8+
- Dependencies: Flask, Pillow, NumPy

### 2. Install Dependencies (安装依赖)
```bash
pip install flask pillow numpy