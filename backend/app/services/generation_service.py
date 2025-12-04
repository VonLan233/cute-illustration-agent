"""
图片生成业务服务 - 整合 LLM 和生图服务
"""

import uuid
from typing import Dict, Optional
from datetime import datetime

from app.services.llm_service import llm_service
from app.services.image_service import image_service
from app.models.schemas import GenerationRequest, RefineRequest


class GenerationService:
    """图片生成业务服务"""

    def __init__(self):
        # 内存存储（生产环境应使用数据库）
        self._generations: Dict[str, dict] = {}

    def _generate_id(self) -> str:
        """生成唯一ID"""
        return f"gen_{uuid.uuid4().hex[:12]}"

    async def generate(self, request: GenerationRequest) -> dict:
        """
        完整生成流程：需求 -> 提示词优化 -> 生图 -> 返回结果

        Args:
            request: 生成请求

        Returns:
            生成结果
        """
        generation_id = self._generate_id()

        # 1. LLM 优化提示词
        optimized_prompt = await llm_service.optimize_prompt(
            theme=request.theme,
            styles=[s.value for s in request.styles],
            size=request.size.value,
            purpose=request.purpose,
            extra_description=request.extra_description
        )

        # 2. 调用生图 API
        image_result = await image_service.generate_image_with_retry(
            prompt=optimized_prompt,
            size=request.size.value,
            style_strength=request.style_strength
        )

        # 3. 存储生成记录
        generation_record = {
            "generation_id": generation_id,
            "image_url": image_result["image_url"],
            "optimized_prompt": optimized_prompt,
            "original_request": request.model_dump(),
            "seed": image_result.get("seed"),
            "model": image_result.get("model"),
            "created_at": datetime.utcnow().isoformat(),
            "parent_id": None  # 非微调生成
        }
        self._generations[generation_id] = generation_record

        return {
            "generation_id": generation_id,
            "image_url": image_result["image_url"],
            "optimized_prompt": optimized_prompt,
            "original_request": request
        }

    async def refine(self, request: RefineRequest) -> dict:
        """
        微调流程：获取原提示词 -> LLM 微调 -> 重新生图

        Args:
            request: 微调请求

        Returns:
            微调结果
        """
        # 1. 获取原生成记录
        original = self._generations.get(request.generation_id)
        if not original:
            raise ValueError(f"未找到生成记录: {request.generation_id}")

        # 2. LLM 微调提示词
        refined_prompt = await llm_service.refine_prompt(
            original_prompt=original["optimized_prompt"],
            refine_instruction=request.refine_instruction
        )

        # 3. 重新生成图片
        original_request = original["original_request"]
        image_result = await image_service.generate_image_with_retry(
            prompt=refined_prompt,
            size=original_request.get("size", "square_medium"),
            style_strength=original_request.get("style_strength", 0.8)
        )

        # 4. 存储新的生成记录
        new_generation_id = self._generate_id()
        generation_record = {
            "generation_id": new_generation_id,
            "image_url": image_result["image_url"],
            "optimized_prompt": refined_prompt,
            "original_request": original_request,
            "refine_instruction": request.refine_instruction,
            "seed": image_result.get("seed"),
            "model": image_result.get("model"),
            "created_at": datetime.utcnow().isoformat(),
            "parent_id": request.generation_id  # 关联原生成
        }
        self._generations[new_generation_id] = generation_record

        return {
            "generation_id": new_generation_id,
            "image_url": image_result["image_url"],
            "optimized_prompt": refined_prompt,
            "original_generation_id": request.generation_id
        }

    def get_generation(self, generation_id: str) -> Optional[dict]:
        """获取生成记录"""
        return self._generations.get(generation_id)

    def get_generation_history(self, generation_id: str) -> list:
        """获取生成历史链（包括所有微调版本）"""
        history = []
        current_id = generation_id

        # 向上追溯到原始生成
        while current_id:
            record = self._generations.get(current_id)
            if not record:
                break
            history.insert(0, record)
            current_id = record.get("parent_id")

        # 向下查找所有子版本
        children = [
            r for r in self._generations.values()
            if r.get("parent_id") == generation_id
        ]
        history.extend(children)

        return history


# 全局服务实例
generation_service = GenerationService()
