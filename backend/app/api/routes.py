"""
API 路由定义
"""

from fastapi import APIRouter, HTTPException
from typing import List

from app.models.schemas import (
    GenerationRequest,
    GenerationResponse,
    RefineRequest,
    RefineResponse,
    StyleInfo,
    StyleListResponse,
    SizeInfo,
    SizeListResponse,
    ErrorResponse
)
from app.core.styles import STYLE_LIBRARY, SIZE_OPTIONS, PURPOSE_OPTIONS
from app.services.generation_service import generation_service


router = APIRouter()


# ============ 配置接口 ============

@router.get(
    "/styles",
    response_model=StyleListResponse,
    summary="获取所有可用风格",
    description="返回系统预置的所有可爱风格及其特征描述"
)
async def get_styles():
    """获取所有可用风格"""
    styles = []
    for style_id, style_data in STYLE_LIBRARY.items():
        styles.append(StyleInfo(
            id=style_id,
            name=style_data["name"],
            name_en=style_data["name_en"],
            features=style_data["features"],
            keywords_cn=style_data["keywords_cn"],
            keywords_en=style_data["keywords_en"]
        ))
    return StyleListResponse(styles=styles)


@router.get(
    "/sizes",
    response_model=SizeListResponse,
    summary="获取所有可用尺寸",
    description="返回系统支持的所有图片尺寸选项"
)
async def get_sizes():
    """获取所有可用尺寸"""
    sizes = []
    for size_id, size_data in SIZE_OPTIONS.items():
        sizes.append(SizeInfo(
            id=size_id,
            name=size_data["name"],
            size=size_data["size"],
            ratio=size_data["ratio"]
        ))
    return SizeListResponse(sizes=sizes)


@router.get(
    "/purposes",
    summary="获取所有用途场景",
    description="返回预设的用途场景选项"
)
async def get_purposes():
    """获取所有用途场景"""
    return {"purposes": PURPOSE_OPTIONS}


# ============ 生成接口 ============

@router.post(
    "/generate",
    response_model=GenerationResponse,
    summary="生成可爱插图",
    description="根据用户需求生成可爱风格插图，包含自动提示词优化",
    responses={
        500: {"model": ErrorResponse, "description": "生成失败"}
    }
)
async def generate_image(request: GenerationRequest):
    """
    生成可爱插图

    流程：
    1. 接收用户输入（主题、风格、尺寸等）
    2. LLM 优化提示词
    3. 调用生图 API 生成图片
    4. 返回结果
    """
    try:
        result = await generation_service.generate(request)
        return GenerationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/refine",
    response_model=RefineResponse,
    summary="微调图片",
    description="基于已生成的图片进行微调，支持调整质感、比例、颜色等",
    responses={
        404: {"model": ErrorResponse, "description": "原生成记录不存在"},
        500: {"model": ErrorResponse, "description": "微调失败"}
    }
)
async def refine_image(request: RefineRequest):
    """
    微调图片

    流程：
    1. 获取原生成记录的提示词
    2. LLM 根据微调指令修改提示词
    3. 重新调用生图 API
    4. 返回新结果
    """
    try:
        result = await generation_service.refine(request)
        return RefineResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============ 查询接口 ============

@router.get(
    "/generation/{generation_id}",
    summary="获取生成记录",
    description="根据ID获取单个生成记录详情"
)
async def get_generation(generation_id: str):
    """获取生成记录"""
    record = generation_service.get_generation(generation_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"未找到生成记录: {generation_id}")
    return record


@router.get(
    "/generation/{generation_id}/history",
    summary="获取生成历史",
    description="获取某次生成的完整历史链，包括原始生成和所有微调版本"
)
async def get_generation_history(generation_id: str):
    """获取生成历史"""
    history = generation_service.get_generation_history(generation_id)
    if not history:
        raise HTTPException(status_code=404, detail=f"未找到生成记录: {generation_id}")
    return {"history": history}
