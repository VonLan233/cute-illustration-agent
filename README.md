# 可爱插图生成智能体

面向 C 端用户的可爱风格插图生成智能体，让零设计基础的用户也能轻松生成精美可爱插图。

## 功能特性

- **10+ 可爱风格**：Q版漫画、毛绒质感、吉卜力童话、潮玩盲盒、水彩晕染等
- **智能提示词优化**：基于 DeepSeek LLM 自动优化用户输入，补充光影、质感、构图细节
- **高质量生图**：对接豆包 SeeDream 生成精美插图
- **多轮微调**：支持"更胖一点"、"换成毛绒质感"等自然语言微调

## 技术架构

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   用户输入   │ ──> │  DeepSeek    │ ──> │ 豆包SeeDream │
│  (主题/风格) │     │  提示词优化   │     │   生成图片   │
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                           v
                    ┌──────────────┐
                    │   微调迭代    │
                    │  (可选循环)   │
                    └──────────────┘
```

## 快速开始

### 1. 环境准备

```bash
cd cute-illustration-agent/backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置 API 密钥

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入您的 API 密钥：

```env
DEEPSEEK_API_KEY=your_deepseek_api_key
DOUBAO_API_KEY=your_doubao_api_key
```

### 3. 启动服务

```bash
# 方式一：使用启动脚本
chmod +x run.sh
./run.sh

# 方式二：直接启动
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. 访问 API

- API 文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/health

## API 接口

### 获取风格列表

```bash
GET /api/v1/styles
```

### 获取尺寸列表

```bash
GET /api/v1/sizes
```

### 生成图片

```bash
POST /api/v1/generate

{
  "theme": "一只猫咪戴着蝴蝶结",
  "styles": ["q_version", "fluffy"],
  "size": "square_medium",
  "purpose": "social_media",
  "extra_description": "在草地上玩耍，阳光明媚",
  "style_strength": 0.8
}
```

### 微调图片

```bash
POST /api/v1/refine

{
  "generation_id": "gen_abc123",
  "refine_instruction": "更胖一点，换成毛绒质感"
}
```

## 可用风格

| 风格ID | 名称 | 特征 |
|--------|------|------|
| q_version | Q版漫画 | 3-5头身、大头、夸张表情、简洁线条 |
| fluffy | 毛绒质感 | 马卡龙色、蓬松触感、棉花质感 |
| ghibli | 吉卜力童话 | 柔和水彩、自然光影、温暖色调 |
| blind_box | 潮玩盲盒 | PVC哑光、立体感、饱和色彩 |
| watercolor | 水彩晕染 | 柔和边缘、渐变过渡、透明质感 |
| pixel | 像素风 | 8bit风格、方块构成、复古色彩 |
| clay | 黏土手工 | 黏土质感、手工痕迹、圆润造型 |
| pastel | 粉彩梦幻 | 粉彩色系、梦幻柔焦、少女感 |
| flat_design | 扁平插画 | 几何形状、纯色块、简约线条 |
| anime | 日系动漫 | 大眼睛、精致发丝、鲜艳色彩 |
| sticker | 贴纸风格 | 白色描边、简洁造型、表情包风 |
| 3d_render | 3D渲染 | 立体建模、光影层次、高清渲染 |

## 项目结构

```
cute-illustration-agent/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py       # API 路由
│   │   ├── core/
│   │   │   ├── config.py       # 配置管理
│   │   │   └── styles.py       # 风格库定义
│   │   ├── models/
│   │   │   └── schemas.py      # 数据模型
│   │   ├── services/
│   │   │   ├── llm_service.py       # DeepSeek LLM 服务
│   │   │   ├── image_service.py     # 豆包生图服务
│   │   │   └── generation_service.py # 业务逻辑层
│   │   └── templates/
│   │       └── prompts.py      # 提示词模板
│   ├── main.py                 # FastAPI 入口
│   ├── requirements.txt
│   ├── .env.example
│   └── run.sh
└── README.md
```

## 后续扩展

- [ ] 添加 PostgreSQL 持久化存储
- [ ] 实现用户系统和偏好保存
- [ ] 添加图片历史和收藏功能
- [ ] 实现前端 Vue3 界面
- [ ] 支持更多生图模型（Midjourney、DALL-E等）
# cute-illustration-agent
