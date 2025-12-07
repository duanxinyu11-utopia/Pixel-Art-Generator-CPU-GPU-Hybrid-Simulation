import requests
import base64
import json
import os

# 配置：服务器地址和图片路径
url = "http://127.0.0.1:5000/api/pixelate"
img_path = "test.jpg"  # 确保你的文件夹里有这张图！

# 1. 检查图片是否存在
if not os.path.exists(img_path):
    print(f"❌ 错误：找不到文件 {img_path}")
    print("请找一张图片放进项目文件夹，并重命名为 tests.jpg")
    exit()

# 2. 读取并编码图片 (模拟前端上传)
print(f"正在读取 {img_path}...")
with open(img_path, "rb") as img_file:
    # 将二进制图片转为 Base64 字符串
    b64_string = base64.b64encode(img_file.read()).decode('utf-8')

# 3. 构造请求数据
payload = {
    "image": b64_string,
    "mode": "cpu",  # 这里可以改成 'cpu' 来对比速度
    "pixelSize": 16  # 像素块大小，越大越模糊
}

# 4. 发送请求给你的 app.py
print(f"正在发送请求到 {url} (模式: {payload['mode']})...")
try:
    response = requests.post(url, json=payload)

    # 5. 处理响应
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 处理成功！耗时: {result.get('processTime')}")

        # 将返回的 Base64 字符串变回图片文件
        img_data = base64.b64decode(result['pixelArtImage'])
        output_filename = f"output_{payload['mode']}.png"

        with open(output_filename, "wb") as f:
            f.write(img_data)
        print(f"图片已保存为: {output_filename}")
        print("快去文件夹里打开看看效果吧！")
    else:
        print("❌ 失败:", response.text)

except Exception as e:
    print(f"❌ 无法连接服务器: {e}")
    print("请检查 app.py 是否正在运行！")