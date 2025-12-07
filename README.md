Markdown

# 🎨 Pixel Art Generator (IWM2 Complete Version)

## 📖 Project Overview (项目简介)
**Pixel Art Generator** is a full-stack web application that converts uploaded images into retro-style pixel art. 
**像素画生成器** 是一个全栈 Web 应用程序，可以将上传的图像转换为复古风格的像素画。

The project serves as a comprehensive demonstration of **Software Architecture & Performance Engineering**:
本项目作为一个综合演示，展示了 **软件架构与性能工程**：
1.  **Architecture**: Comparing Serial (CPU) vs. Vectorized (GPU) vs. AI Clustering (K-Means). (架构对比)
2.  **DevOps**: Implementation of CI/CD pipelines, Docker containerization, and automated testing. (DevOps 工程化)

---

## 🚀 Features (功能特性)
- **Web Interface**: User-friendly UI for instant image processing. (友好的 Web 界面)
- **Triple Processing Modes (三种处理模式)**:
  - **🐢 CPU Mode**: Standard serial processing using loops (O(N) Complexity).
  - **⚡ GPU Mode**: Simulated parallel processing using NumPy vectorization (Fast).
  - **🤖 AI Mode (New)**: Uses **K-Means Clustering** (Machine Learning) to intelligently extract dominant color palettes for a more artistic look. (新增 AI 聚类模式)
- **Engineering Standards**: Fully tested with Pytest and linted with Flake8.

---

## 🛠️ Installation & Setup (安装与运行)

You can run this project locally or using Docker.
你可以选择本地运行或使用 Docker 运行。

### Method 1: Docker (Recommended)
This ensures the application runs flawlessly in an isolated environment.
这是推荐方式，确保应用在隔离环境中完美运行。

```bash
# 1. Build the Docker image (构建镜像)
docker build -t pixel-art-app .

# 2. Run the container (运行容器)
docker run -p 5000:5000 pixel-art-app
Visit (访问): http://127.0.0.1:5000

Method 2: Local Python Setup (本地运行)
Prerequisites: Python 3.8+

Bash

# 1. Install dependencies (安装依赖)
pip install -r requirements.txt

# 2. Run the application (启动应用)
python app.py
🧪 Testing & CI/CD (测试与自动化)
This project maintains high code quality through automated pipelines. 本项目通过自动化流水线保持高质量代码。

Run Tests Locally (本地运行测试)
We use pytest for both unit and integration tests.

Bash

# Run all tests
python -m pytest
CI/CD Pipeline (GitHub Actions)
Every push to the main branch triggers an automated workflow that: 每次推送到 main 分支都会触发自动工作流：

Lints the code using flake8. (代码风格检查)

Tests the core logic and API using pytest. (自动化测试)

🔬 Technical Deep Dive (技术深度解析)
Why K-Means? (为什么引入 K-Means?)
While the CPU/GPU modes simply calculate the average color of a block, the AI Mode uses Unsupervised Machine Learning. It clusters pixels to find the most representative colors, creating a result that looks more like hand-drawn pixel art rather than just a blurry image. CPU/GPU 模式仅计算块的平均颜色，而 AI 模式使用无监督机器学习。它通过聚类找到最具代表性的颜色，生成的图像更像手绘像素画，而不是简单的模糊图像。

📂 Project Structure (项目结构)
Plaintext

/PixelArt
├── .github/workflows/   # CI/CD Configuration (CI配置)
├── screenshots/         # Demo & Test Evidence (截图证据)
├── templates/           # Frontend HTML (前端页面)
├── tests/               # Automated Tests (测试代码)
├── app.py               # Flask Backend (后端入口)
├── processor.py         # Core Algorithms (CPU/GPU/AI Logic)
├── Dockerfile           # Container Config (Docker配置)
└── requirements.txt     # Dependencies (依赖列表)
👤 Author
Duan Xinyu IWM2 Final Submission - Hybrid CPU/GPU/AI Simulation