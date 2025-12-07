import pytest
import numpy as np
from PIL import Image
from processor import PixelArtGenerator

# 创建一个 100x100 的随机噪点图片用于测试
@pytest.fixture
def dummy_image():
    arr = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    return Image.fromarray(arr)

def test_initialization(dummy_image):
    """测试类是否能正确初始化"""
    gen = PixelArtGenerator(dummy_image, pixel_size=10)
    assert gen.width == 100
    assert gen.height == 100
    assert gen.cols == 10  # 100 / 10 = 10

def test_process_cpu_output_size(dummy_image):
    """测试 CPU 模式输出的尺寸是否正确"""
    gen = PixelArtGenerator(dummy_image, pixel_size=10)
    result = gen.process_cpu()
    # 尺寸应该和原图一样
    assert result.size == (100, 100)
    # 必须是 PIL Image 对象
    assert isinstance(result, Image.Image)

def test_process_gpu_output_size(dummy_image):
    """测试 GPU 模式输出的尺寸是否正确"""
    gen = PixelArtGenerator(dummy_image, pixel_size=10)
    result = gen.process_gpu_simulated()
    assert result.size == (100, 100)

def test_process_kmeans_runs(dummy_image):
    """测试 K-Means 模式是否能正常运行不报错"""
    gen = PixelArtGenerator(dummy_image, pixel_size=10)
    # 只要不报错就算通过
    result = gen.process_kmeans(n_colors=4)
    assert result.size == (100, 100)