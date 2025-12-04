"""
Pydantic 数据模型定义
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class StyleEnum(str, Enum):
    """可用风格枚举"""
    Q_VERSION = "q_version"
    FLUFFY = "fluffy"
    GHIBLI = "ghibli"
    BLIND_BOX = "blind_box"
    WATERCOLOR = "watercolor"
    PIXEL = "pixel"
    CLAY = "clay"
    PASTEL = "pastel"
    FLAT_DESIGN = "flat_design"
    ANIME = "anime"
    STICKER = "sticker"
    THREE_D_RENDER = "3d_render"


class SizeEnum(str, Enum):
    """可用尺寸枚举"""
    SQUARE_SMALL = "square_small"
    SQUARE_MEDIUM = "square_medium"
    LANDSCAPE_HD = "landscape_hd"
    PORTRAIT_HD = "portrait_hd"
    LANDSCAPE_2K = "landscape_2k"
    SOCIAL_POST = "social_post"
    AVATAR = "avatar"


class GenerationRequest(BaseModel):
    """生成请求模型"""
    theme: str = Field(..., description="主题描述", min_length=1, max_length=200)
    styles: List[StyleEnum] = Field(..., description="风格标签列表", min_length=1)
    size: SizeEnum = Field(default=SizeEnum.SQUARE_MEDIUM, description="图片尺寸")
    purpose: Optional[str] = Field(default=None, description="用途场景")
    extra_description: Optional[str] = Field(default=None, description="额外自由描述", max_length=500)
    style_strength: float = Field(default=0.8, ge=0.1, le=1.0, description="风格强度")

    class Config:
        json_schema_extra = {
            "example": {
                "theme": "一只猫咪戴着蝴蝶结",
                "styles": ["q_version", "fluffy"],
                "size": "square_medium",
                "purpose": "social_media",
                "extra_description": "在草地上玩耍，阳光明媚",
                "style_strength": 0.8
            }
        }


class RefineRequest(BaseModel):
    """微调请求模型"""
    generation_id: str = Field(..., description="原生成记录ID")
    refine_instruction: str = Field(..., description="微调指令", min_length=1, max_length=200)

    class Config:
        json_schema_extra = {
            "example": {
                "generation_id": "gen_abc123",
                "refine_instruction": "更胖一点，换成毛绒质感"
            }
        }


class PromptOptimizeRequest(BaseModel):
    """提示词优化请求（内部使用）"""
    theme: str
    styles: List[str]
    size: str
    purpose: Optional[str] = None
    extra_description: Optional[str] = None


class PromptRefineRequest(BaseModel):
    """提示词微调请求（内部使用）"""
    original_prompt: str
    refine_instruction: str


class GenerationResponse(BaseModel):
    """生成响应模型"""
    generation_id: str = Field(..., description="生成记录ID")
    image_url: str = Field(..., description="生成图片URL")
    optimized_prompt: str = Field(..., description="优化后的提示词")
    original_request: GenerationRequest = Field(..., description="原始请求")

    class Config:
        json_schema_extra = {
            "example": {
                "generation_id": "gen_abc123",
                "image_url": "https://example.com/image.png",
                "optimized_prompt": "Q版大头身可爱猫咪...",
                "original_request": {
                    "theme": "一只猫咪戴着蝴蝶结",
                    "styles": ["q_version"],
                    "size": "square_medium"
                }
            }
        }


class RefineResponse(BaseModel):
    """微调响应模型"""
    generation_id: str = Field(..., description="新生成记录ID")
    image_url: str = Field(..., description="新生成图片URL")
    optimized_prompt: str = Field(..., description="微调后的提示词")
    original_generation_id: str = Field(..., description="原生成记录ID")


class StyleInfo(BaseModel):
    """风格信息模型"""
    id: str
    name: str
    name_en: str
    features: List[str]
    keywords_cn: str
    keywords_en: str


class StyleListResponse(BaseModel):
    """风格列表响应"""
    styles: List[StyleInfo]


class SizeInfo(BaseModel):
    """尺寸信息模型"""
    id: str
    name: str
    size: str
    ratio: str


class SizeListResponse(BaseModel):
    """尺寸列表响应"""
    sizes: List[SizeInfo]


class ErrorResponse(BaseModel):
    """错误响应模型"""
    error: str
    detail: Optional[str] = None
