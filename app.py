import base64
import io
import time
from flask import Flask, request, jsonify, render_template
from PIL import Image
from processor import PixelArtGenerator  # Import the core processing class

app = Flask(__name__)


@app.route('/')
def index():
    """
    Renders the main page (Frontend).
    """
    return render_template('index.html')


# --- Utility Helper Functions ---

def decode_image(base64_string):
    """
    Decodes a Base64 string received from the frontend into a PIL Image object.

    Args:
        base64_string (str): The raw base64 string (may include data URI header).

    Returns:
        Image: A PIL Image object in RGB mode.
    """
    # Remove the data URI header (e.g., "data:image/png;base64,") if present
    if "," in base64_string:
        base64_string = base64_string.split(",")[1]

    # Decode base64 string to bytes
    image_data = base64.b64decode(base64_string)

    # Convert bytes to a PIL Image
    return Image.open(io.BytesIO(image_data)).convert('RGB')


def encode_image(image):
    """
    Encodes a PIL Image object back into a Base64 string to send to the frontend.

    Args:
        image (Image): The processed PIL Image object.

    Returns:
        str: Base64 encoded string of the image.
    """
    buffered = io.BytesIO()
    # Save image to the memory buffer as PNG
    image.save(buffered, format="PNG")
    # Encode bytes to base64 string
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return img_str


# --- API Routes ---

# ... 前面的代码保持不变 ...

@app.route('/api/pixelate', methods=['POST'])
def pixelate():
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({"error": "No image data found"}), 400

    mode = data.get('mode', 'cpu')
    pixel_size = int(data.get('pixelSize', 8))

    try:
        original_image = decode_image(data['image'])
        generator = PixelArtGenerator(original_image, pixel_size)
        start_time = time.time()

        # --- 修改了这里：增加了 kmeans 判断 ---
        if mode == 'gpu':
            processed_image = generator.process_gpu_simulated()
            process_type = "GPU (Vectorized)"
        elif mode == 'kmeans':
            # K-Means 模式：AI 聚类，颜色更鲜艳
            processed_image = generator.process_kmeans(n_colors=16)
            process_type = "AI (K-Means Clustering)"
        else:
            processed_image = generator.process_cpu()
            process_type = "CPU (Serial)"
        # ------------------------------------

        duration = time.time() - start_time
        print(f"Mode: {process_type} | Time taken: {duration:.4f}s")

        result_base64 = encode_image(processed_image)
        return jsonify({
            "pixelArtImage": result_base64,
            "mode": mode,
            "processTime": f"{duration:.4f}s"
        }), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


# ... 后面的代码保持不变 ...


if __name__ == '__main__':
    # Start the Flask development server
    app.run(debug=True, port=5000)