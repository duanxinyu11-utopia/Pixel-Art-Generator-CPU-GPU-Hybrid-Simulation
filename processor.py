import numpy as np
from PIL import Image
from sklearn.cluster import MiniBatchKMeans  # 引入机器学习库


class PixelArtGenerator:
    def __init__(self, image_pil, pixel_size):
        self.image = image_pil
        self.pixel_size = pixel_size
        self.width, self.height = image_pil.size
        self.cols = self.width // pixel_size
        self.rows = self.height // pixel_size

    def process_cpu(self):
        """标准 CPU 模式：基于循环的均值计算"""
        pixels = np.array(self.image)
        output = np.zeros_like(pixels)
        for r in range(self.rows):
            for c in range(self.cols):
                r_start = r * self.pixel_size
                c_start = c * self.pixel_size
                r_end = r_start + self.pixel_size
                c_end = c_start + self.pixel_size
                block = pixels[r_start:r_end, c_start:c_end]
                if block.size > 0:
                    avg_color = np.mean(block, axis=(0, 1)).astype(int)
                    output[r_start:r_end, c_start:c_end] = avg_color
        return Image.fromarray(output)

    def process_gpu_simulated(self):
        """GPU 模拟模式：向量化并行计算"""
        pixels = np.array(self.image)
        h_trim = self.rows * self.pixel_size
        w_trim = self.cols * self.pixel_size
        pixels = pixels[:h_trim, :w_trim]
        reshaped = pixels.reshape(self.rows, self.pixel_size, self.cols, self.pixel_size, 3)
        avg_colors = reshaped.mean(axis=(1, 3)).astype(np.uint8)
        output = avg_colors.repeat(self.pixel_size, axis=0).repeat(self.pixel_size, axis=1)
        return Image.fromarray(output)

    def process_kmeans(self, n_colors=8):
        """
        【新增高级功能】K-Means 聚类算法 (AI 风格化)
        原理：不是简单的取平均值，而是找出图片中最具代表性的 k 种颜色。
        """
        # 1. 将图片转为像素点列表 (N, 3)
        img_array = np.array(self.image)
        w, h, d = img_array.shape
        pixels = img_array.reshape((w * h, d))

        # 2. 使用机器学习模型聚类
        kmeans = MiniBatchKMeans(n_clusters=n_colors, batch_size=2048, n_init='auto')
        labels = kmeans.fit_predict(pixels)

        # 3. 用聚类中心颜色替换原始颜色
        new_colors = kmeans.cluster_centers_.astype('uint8')
        new_pixels = new_colors[labels]

        # 4. 还原为图片形状
        output = new_pixels.reshape((w, h, d))

        # 5. 再次应用像素化（为了保持像素风格）
        # 这里递归调用基础的像素化逻辑，但基于新的颜色
        temp_img = Image.fromarray(output)
        # 这里我们在内部临时创建一个小实例来做最后一步像素化
        temp_generator = PixelArtGenerator(temp_img, self.pixel_size)
        return temp_generator.process_gpu_simulated()