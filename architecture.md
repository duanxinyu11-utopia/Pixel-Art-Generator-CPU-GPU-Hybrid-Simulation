# 🏗️ System Architecture & Design Document (系统架构设计文档)

## 1. High-Level Architecture (顶层架构)
The project follows a variation of the **Model-View-Controller (MVC)** design pattern, adapted for a lightweight Flask application.
本项目采用了 **MVC (模型-视图-控制器)** 设计模式的变体，适配于轻量级 Flask 应用。

- **Model (Logic)**: `processor.py`
  - Encapsulates all image processing algorithms (CPU/GPU/AI).
  - Pure Python/NumPy logic, independent of the web framework.
- **View (Frontend)**: `templates/index.html`
  - Handles user interaction and image preview.
  - Uses Client-Side Rendering (JavaScript) to update results asynchronously.
- **Controller (API)**: `app.py`
  - Manages HTTP requests and routes data between the Frontend and the Processor.

---

## 2. Component Detail (组件详解)

### 2.1 Core Processor (`processor.py`)
This is the computational engine of the application. It implements the **Strategy Pattern** implicitly by offering multiple processing modes for the same input.
这是应用的计算引擎。它通过为同一输入提供多种处理模式，隐式地实现了**策略模式**。

* **`process_cpu()`**: 
    * **Algorithm**: Sliding window average.
    * **Implementation**: Nested `for` loops iterating `(row, col)`.
    * **Performance**: Low. complexity is $O(N)$ but with high Python interpreter overhead.
    
* **`process_gpu_simulated()`**: 
    * **Algorithm**: Tensor reduction.
    * **Implementation**: 
        1.  Reshapes image tensor: $(H, W, 3) \rightarrow (rows, block\_size, cols, block\_size, 3)$
        2.  Performs `mean` reduction on axis 1 and 3 simultaneously.
    * **Performance**: High. Leverages BLAS/LAPACK optimized C libraries via NumPy.

* **`process_kmeans()`**: 
    * **Algorithm**: Unsupervised Clustering (Mini-Batch K-Means).
    * **Implementation**: Flattens image to $(N, 3)$, groups pixels into $K$ clusters, and reconstructs the image using cluster centers.

### 2.2 Web Controller (`app.py`)
Serves as the RESTful API gateway.
作为 RESTful API 网关。

* **`pixelate()` Endpoint**:
    * **Input**: JSON payload `{ "image": "base64...", "mode": "cpu|gpu|kmeans" }`.
    * **Responsibility**: 
        1.  Validates input.
        2.  Deserializes Base64 to PIL Image.
        3.  Dispatches task to `PixelArtGenerator`.
        4.  Measures execution time.
        5.  Serializes output back to JSON.

### 2.3 Frontend Client (`index.html`)
A Single Page Application (SPA) logic without using heavy frameworks.
不依赖重型框架的单页应用逻辑。

* **Workflow**:
    1.  User selects image -> `FileReader` API previews it locally.
    2.  User clicks "Generate" -> `fetch()` API sends async POST request.
    3.  Server responds -> JavaScript updates the `src` attribute of the result image.
* **Optimization**: Base64 encoding is used to avoid multipart file uploads, simplifying the deployment structure.

---

## 3. Data Flow Diagram (数据流图)

```text
[User] 
  ⬇️ (Uploads Image)
[Browser (index.html)] 
  ⬇️ (Converts to Base64 JSON)
  ⬇️ (HTTP POST /api/pixelate)
[Flask Server (app.py)] 
  ⬇️ (Decodes Image)
[PixelArtGenerator (processor.py)]
  ⬇️ 
  ├─> CPU Mode: Loops
  ├─> GPU Mode: Matrix Ops
  └─> AI Mode: K-Means
  ⬇️ (Returns Processed Image)
[Flask Server] 
  ⬇️ (Encodes to Base64)
  ⬇️ (JSON Response)
[Browser] 
  ⬇️ (Updates DOM)
[User sees Result]