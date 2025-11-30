import numpy as np
from PIL import Image


class PixelArtGenerator:
    def __init__(self, image_pil, pixel_size):
        """
        初始化生成器
        :param image_pil: 传入的 PIL 图像对象
        :param pixel_size: 像素块的大小 (比如 8 代表 8x8 的像素合并为一个格)
        """
        self.image = image_pil
        self.pixel_size = pixel_size
        self.width, self.height = image_pil.size
        # 计算横向和纵向有多少个格子
        self.cols = self.width // pixel_size
        self.rows = self.height // pixel_size

    def process_cpu(self):
        """
        【CPU 模式】模拟串行处理
        原理：使用 Python 的 for 循环逐个遍历像素块。
        这在 Python 中是很慢的，正好用来体现 CPU 串行处理大量数据的劣势。
        """
        # 将图片转为 numpy 数组以便读取数值
        pixels = np.array(self.image)
        output = np.zeros_like(pixels)  # 创建一个全黑的画布

        # 双重循环：一个一个格子地处理
        for r in range(self.rows):
            for c in range(self.cols):
                # 1. 定位当前格子的坐标范围
                r_start = r * self.pixel_size
                c_start = c * self.pixel_size
                r_end = r_start + self.pixel_size
                c_end = c_start + self.pixel_size

                # 2. 提取这个格子的所有像素
                block = pixels[r_start:r_end, c_start:c_end]

                # 3. 计算平均颜色 (CPU 逐块计算)
                if block.size > 0:
                    avg_color = np.mean(block, axis=(0, 1)).astype(int)

                    # 4. 把平均色填回画布
                    output[r_start:r_end, c_start:c_end] = avg_color

        return Image.fromarray(output)

    def process_gpu_simulated(self):
        """
        【GPU 模拟模式】向量化并行处理
        原理：不使用任何 for 循环，而是利用 NumPy 的矩阵运算一次性算出所有结果。
        这模拟了 GPU 几千个核心同时工作的场景 (SIMD)。
        """
        pixels = np.array(self.image)

        # 1. 裁剪图片，确保尺寸能被 pixel_size 整除 (矩阵运算要求形状整齐)
        h_trim = self.rows * self.pixel_size
        w_trim = self.cols * self.pixel_size
        pixels = pixels[:h_trim, :w_trim]

        # 2. 【核心魔法】Reshape (改变维度)
        # 将图片从 (H, W, 3) 变成 (行数, 格子高, 列数, 格子宽, 3)
        # 这样就把“所有的格子”在维度上对齐了
        reshaped = pixels.reshape(self.rows, self.pixel_size, self.cols, self.pixel_size, 3)

        # 3. 【并行计算】一次性求出所有格子的平均值
        # axis=(1, 3) 代表在“格子高”和“格子宽”这两个维度上取平均
        avg_colors = reshaped.mean(axis=(1, 3)).astype(np.uint8)

        # 4. 【广播填充】将算出的颜色扩充回原来的像素大小
        # 类似于把 1x1 的颜色块放大回 8x8
        output = avg_colors.repeat(self.pixel_size, axis=0).repeat(self.pixel_size, axis=1)

        return Image.fromarray(output)