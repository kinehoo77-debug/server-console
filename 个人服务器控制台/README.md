# server-console

轻量级个人服务器 WEB 控制台，集成系统监控、可视化文件管理、系统日志查看和 Docker 面板快捷跳转。

## 功能

- 系统监控仪表盘
  - CPU 实时折线图（ECharts）
  - 内存环形图 + 数值
  - 磁盘环形图 + 数值
  - 系统信息：IP、版本、运行时间、负载
  - 网络吞吐实时显示
- 可视化文件管理器
  - 目录浏览（类似资源管理器）
  - 拖拽上传 / 点击上传
  - 下载、删除、重命名、新建文件夹
  - 文本文件在线预览/编辑
  - 图片在线预览
- 系统日志
  - 实时刷新
  - 搜索
  - 清空当前视图
- Docker 面板快捷跳转
  - `http://38.76.188.104:7080/`
- 安全登录
  - 单管理员密码登录
  - 会话保持和退出

## 技术栈

- 后端：Flask
- 前端：Bootstrap 5 + ECharts + 原生 JavaScript
- 监控：psutil
- 部署：Docker Compose
- 端口：7010

## 目录结构

```text
个人服务器控制台/
├─ app/
│  ├─ routes/
│  │  ├─ auth.py
│  │  └─ main.py
│  ├─ services/
│  │  ├─ monitor_service.py
│  │  ├─ file_service.py
│  │  └─ log_service.py
│  ├─ utils/
│  │  ├─ auth.py
│  │  └─ response.py
│  ├─ templates/
│  │  ├─ base.html
│  │  ├─ login.html
│  │  ├─ dashboard.html
│  │  ├─ files.html
│  │  └─ logs.html
│  ├─ static/
│  │  ├─ css/style.css
│  │  └─ js/
│  │     ├─ common.js
│  │     ├─ dashboard.js
│  │     ├─ files.js
│  │     └─ logs.js
│  ├─ __init__.py
│  └─ config.py
├─ docs/screenshots/.gitkeep
├─ .env.example
├─ .gitignore
├─ Dockerfile
├─ docker-compose.yml
├─ requirements.txt
├─ run.py
└─ README.md
```

## 本地运行

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Linux/macOS:

```bash
export SECRET_KEY="your-secret"
export ADMIN_PASSWORD="your-strong-password"
export PORT=7010
export FILE_ROOT="/"
python run.py
```

Windows PowerShell:

```powershell
$env:SECRET_KEY="your-secret"
$env:ADMIN_PASSWORD="your-strong-password"
$env:PORT="7010"
$env:FILE_ROOT="D:\"
python run.py
```

访问：`http://127.0.0.1:7010`

## Docker Compose 部署

修改 `docker-compose.yml` 中的 `SECRET_KEY` 和 `LOG_FILE` 后执行：

```bash
docker compose up -d --build
docker compose ps
docker compose logs -f
```

访问：`http://<服务器IP>:7010`

## 环境变量

- `SECRET_KEY`：Flask 会话密钥
- `ADMIN_PASSWORD`：管理员密码
- `FILE_ROOT`：文件管理器根目录
- `LOG_FILE`：日志文件路径
- `MAX_UPLOAD_MB`：上传大小限制（MB）
- `DOCKER_PANEL_URL`：Docker 面板地址

## 截图占位

- `docs/screenshots/dashboard.png`
- `docs/screenshots/files.png`
- `docs/screenshots/logs.png`
