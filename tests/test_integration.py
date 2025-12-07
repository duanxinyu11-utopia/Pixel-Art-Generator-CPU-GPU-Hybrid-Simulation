import pytest
import json
import base64
import io
from PIL import Image
from app import app  # 导入你的 Flask app


@pytest.fixture
def client():
    # 配置 Flask 为测试模式
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def create_dummy_base64_image():
    """创建一个 1x1 的红色图片 Base64 字符串用于发送"""
    img = Image.new('RGB', (100, 100), color='red')
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')


def test_api_pixelate_success(client):
    """测试 API 能够正确响应 200"""
    img_b64 = create_dummy_base64_image()
    payload = {
        "image": img_b64,
        "mode": "cpu",
        "pixelSize": 10
    }

    response = client.post('/api/pixelate',
                           data=json.dumps(payload),
                           content_type='application/json')

    assert response.status_code == 200
    data = response.get_json()
    assert "pixelArtImage" in data
    assert "processTime" in data
    assert data["mode"] == "cpu"


def test_api_invalid_request(client):
    """测试如果没传图片，API 是否报错 400"""
    payload = {"mode": "cpu"}  # 缺少 image 字段
    response = client.post('/api/pixelate',
                           data=json.dumps(payload),
                           content_type='application/json')
    assert response.status_code == 400