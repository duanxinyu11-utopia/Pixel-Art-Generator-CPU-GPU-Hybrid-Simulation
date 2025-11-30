import base64
import io
import time
from flask import Flask, request, jsonify, render_template
from PIL import Image
from processor import PixelArtGenerator  # 导入刚才写的类

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')


# --- 辅助工具函数 ---

def decode_image(base64_string):
    """把前端传来的 Base64 字符串变成图片对象"""
    if "," in base64_string:
        base64_string = base64_string.split(",")[1]
    image_data = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(image_data)).convert('RGB')


def encode_image(image):
    """把处理好的图片对象变回 Base64 字符串发给前端"""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return img_str


# --- API 路由 ---

@app.route('/api/pixelate', methods=['POST'])
def pixelate():
    print("收到请求...")
    data = request.get_json()

    # 1. 检查参数
    if not data or 'image' not in data:
        return jsonify({"error": "没有找到图片数据"}), 400

    # 获取参数，如果没有传则使用默认值
    mode = data.get('mode', 'cpu')  # 模式: 'cpu' 或 'gpu'
    pixel_size = int(data.get('pixelSize', 8))  # 像素块大小

    try:
        # 2. 解码图片
        original_image = decode_image(data['image'])

        # 3. 初始化处理器
        generator = PixelArtGenerator(original_image, pixel_size)

        start_time = time.time()

        # 4. 根据模式执行不同的算法
        if mode == 'gpu':
            processed_image = generator.process_gpu_simulated()
            process_type = "GPU (向量化加速)"
        else:
            processed_image = generator.process_cpu()
            process_type = "CPU (串行循环)"

        duration = time.time() - start_time
        print(f"模式: {process_type} | 耗时: {duration:.4f} 秒")

        # 5. 返回结果
        result_base64 = encode_image(processed_image)
        return jsonify({
            "pixelArtImage": result_base64,
            "mode": mode,
            "processTime": f"{duration:.4f}s"
        }), 200

    except Exception as e:
        print(f"发生错误: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # 启动服务器
    app.run(debug=True, port=5000)