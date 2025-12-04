"""
可爱风格库 - 预置10+主流可爱风格及其核心特征
"""

from typing import Dict, List


STYLE_LIBRARY: Dict[str, Dict] = {
    "q_version": {
        "name": "Q版漫画",
        "name_en": "Chibi/Q-version",
        "features": ["3-5头身比例", "大头", "夸张表情", "简洁线条", "圆润轮廓"],
        "keywords_cn": "Q版, 大头身, 卡通, 可爱比例, 夸张表情, 简洁线条",
        "keywords_en": "chibi, big head, cartoon style, cute proportion, exaggerated expression, simple lines",
        "lighting": "柔和平光",
        "texture": "平涂色块"
    },
    "fluffy": {
        "name": "毛绒质感",
        "name_en": "Fluffy/Plush",
        "features": ["马卡龙色系", "蓬松触感", "棉花质感", "针脚缝线纹理", "柔软感"],
        "keywords_cn": "毛绒, 蓬松, 棉花质感, 针脚缝线, 马卡龙色, 柔软",
        "keywords_en": "fluffy, plush, cotton texture, stitch details, macaron colors, soft",
        "lighting": "暖光柔焦",
        "texture": "毛绒蓬松触感"
    },
    "ghibli": {
        "name": "吉卜力童话",
        "name_en": "Ghibli Style",
        "features": ["柔和水彩", "自然光影", "温暖色调", "手绘质感", "梦幻氛围"],
        "keywords_cn": "吉卜力风格, 宫崎骏, 手绘水彩, 温暖色调, 童话感, 自然光影",
        "keywords_en": "Ghibli style, Miyazaki, hand-painted watercolor, warm tones, fairytale, natural lighting",
        "lighting": "自然柔光",
        "texture": "水彩晕染"
    },
    "blind_box": {
        "name": "潮玩盲盒",
        "name_en": "Designer Toy/Blind Box",
        "features": ["PVC哑光质感", "立体感强", "饱和色彩", "光滑表面", "收藏级精致"],
        "keywords_cn": "盲盒, 潮玩, PVC材质, 哑光质感, 立体, 饱和色彩, 精致",
        "keywords_en": "blind box, designer toy, PVC material, matte texture, 3D, saturated colors, exquisite",
        "lighting": "摄影棚灯光",
        "texture": "PVC哑光"
    },
    "watercolor": {
        "name": "水彩晕染",
        "name_en": "Watercolor",
        "features": ["柔和边缘", "渐变过渡", "透明质感", "水痕效果", "清新感"],
        "keywords_cn": "水彩, 晕染, 渐变, 透明感, 水痕, 清新, 柔和边缘",
        "keywords_en": "watercolor, gradient, transparent, water stain effect, fresh, soft edges",
        "lighting": "自然散射光",
        "texture": "水彩纸质感"
    },
    "pixel": {
        "name": "像素风",
        "name_en": "Pixel Art",
        "features": ["8bit风格", "方块构成", "复古色彩", "锐利边缘", "怀旧感"],
        "keywords_cn": "像素, 8bit, 复古游戏风, 方块, 怀旧",
        "keywords_en": "pixel art, 8-bit, retro game style, blocky, nostalgic",
        "lighting": "平面光",
        "texture": "像素方块"
    },
    "clay": {
        "name": "黏土手工",
        "name_en": "Clay/Plasticine",
        "features": ["黏土质感", "手工痕迹", "圆润造型", "柔和色彩", "立体感"],
        "keywords_cn": "黏土, 橡皮泥, 手工, 圆润, 立体, 柔和色彩",
        "keywords_en": "clay, plasticine, handmade, rounded, 3D, soft colors",
        "lighting": "柔和顶光",
        "texture": "黏土哑光"
    },
    "pastel": {
        "name": "粉彩梦幻",
        "name_en": "Pastel Dream",
        "features": ["粉彩色系", "梦幻柔焦", "少女感", "甜美氛围", "柔光效果"],
        "keywords_cn": "粉彩, 梦幻, 柔焦, 少女风, 甜美, 柔光",
        "keywords_en": "pastel colors, dreamy, soft focus, girly, sweet, soft glow",
        "lighting": "梦幻柔光",
        "texture": "朦胧柔和"
    },
    "flat_design": {
        "name": "扁平插画",
        "name_en": "Flat Illustration",
        "features": ["几何形状", "纯色块", "简约线条", "现代感", "无阴影"],
        "keywords_cn": "扁平, 几何, 纯色块, 简约, 现代, 矢量风格",
        "keywords_en": "flat design, geometric, solid colors, minimal, modern, vector style",
        "lighting": "无阴影",
        "texture": "纯色平涂"
    },
    "anime": {
        "name": "日系动漫",
        "name_en": "Anime Style",
        "features": ["大眼睛", "精致发丝", "动态线条", "鲜艳色彩", "二次元"],
        "keywords_cn": "动漫, 日系, 大眼睛, 精致, 二次元, 鲜艳色彩",
        "keywords_en": "anime, Japanese style, big eyes, detailed hair, vibrant colors, 2D",
        "lighting": "动漫高光",
        "texture": "赛璐璐质感"
    },
    "sticker": {
        "name": "贴纸风格",
        "name_en": "Sticker Style",
        "features": ["白色描边", "简洁造型", "表情包风", "高对比", "圆角设计"],
        "keywords_cn": "贴纸, 表情包, 白色描边, 简洁, 高对比, 圆角",
        "keywords_en": "sticker, emoji style, white outline, simple, high contrast, rounded corners",
        "lighting": "平面光",
        "texture": "光滑贴纸"
    },
    "3d_render": {
        "name": "3D渲染",
        "name_en": "3D Render",
        "features": ["立体建模", "光影层次", "材质细节", "圆润造型", "高清渲染"],
        "keywords_cn": "3D渲染, 立体, Blender风格, 光影层次, 圆润, 高清",
        "keywords_en": "3D render, Blender style, volumetric lighting, smooth, high quality render",
        "lighting": "三点布光",
        "texture": "光滑材质"
    }
}


# 图片尺寸配置
SIZE_OPTIONS: Dict[str, Dict] = {
    "square_small": {"name": "小正方形", "size": "512x512", "ratio": "1:1"},
    "square_medium": {"name": "中正方形", "size": "1024x1024", "ratio": "1:1"},
    "landscape_hd": {"name": "横版高清", "size": "1920x1080", "ratio": "16:9"},
    "portrait_hd": {"name": "竖版高清", "size": "1080x1920", "ratio": "9:16"},
    "landscape_2k": {"name": "横版2K", "size": "2560x1440", "ratio": "16:9"},
    "social_post": {"name": "社交媒体", "size": "1080x1080", "ratio": "1:1"},
    "avatar": {"name": "头像", "size": "512x512", "ratio": "1:1"},
}


# 用途场景
PURPOSE_OPTIONS: List[Dict] = [
    {"id": "social_media", "name": "社交媒体配图"},
    {"id": "avatar", "name": "头像/个人形象"},
    {"id": "sticker", "name": "表情包/贴纸"},
    {"id": "article", "name": "文章配图"},
    {"id": "product", "name": "产品宣传"},
    {"id": "gift", "name": "礼物/贺卡"},
    {"id": "print", "name": "印刷品"},
    {"id": "other", "name": "其他"},
]


def get_style_by_id(style_id: str) -> Dict:
    """根据ID获取风格详情"""
    return STYLE_LIBRARY.get(style_id, {})


def get_all_styles() -> Dict[str, Dict]:
    """获取所有风格"""
    return STYLE_LIBRARY


def get_style_keywords(style_id: str, lang: str = "cn") -> str:
    """获取风格关键词"""
    style = STYLE_LIBRARY.get(style_id, {})
    if lang == "en":
        return style.get("keywords_en", "")
    return style.get("keywords_cn", "")
