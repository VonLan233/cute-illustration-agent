"""
DeepSeek LLM 服务 - 提示词优化
"""

import httpx
from typing import Optional
from app.core.config import settings
from app.core.styles import get_style_by_id, SIZE_OPTIONS
from app.templates.prompts import (
    PROMPT_OPTIMIZER_SYSTEM,
    PROMPT_OPTIMIZER_USER,
    REFINE_SYSTEM,
    REFINE_USER
)


class LLMService:
    """DeepSeek LLM 服务类"""

    def __init__(self):
        self.api_key = settings.deepseek_api_key
        self.base_url = settings.deepseek_base_url
        self.model = "deepseek-chat"

    async def _call_api(self, system_prompt: str, user_prompt: str) -> str:
        """调用 DeepSeek API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()

    def _format_styles(self, style_ids: list) -> str:
        """格式化风格信息"""
        style_descriptions = []
        for style_id in style_ids:
            style = get_style_by_id(style_id)
            if style:
                features = "、".join(style.get("features", []))
                style_descriptions.append(f"{style['name']}({features})")
        return "；".join(style_descriptions) if style_descriptions else "可爱风格"

    def _format_size(self, size_id: str) -> str:
        """格式化尺寸信息"""
        size_info = SIZE_OPTIONS.get(size_id, {})
        return f"{size_info.get('name', '')} {size_info.get('size', '')} ({size_info.get('ratio', '')})"

    async def optimize_prompt(
        self,
        theme: str,
        styles: list,
        size: str,
        purpose: Optional[str] = None,
        extra_description: Optional[str] = None
    ) -> str:
        """
        优化用户输入，生成精准的图像生成提示词

        Args:
            theme: 主题描述
            styles: 风格ID列表
            size: 尺寸ID
            purpose: 用途场景
            extra_description: 额外描述

        Returns:
            优化后的英文提示词
        """
        # 格式化用户输入
        formatted_styles = self._format_styles(styles)
        formatted_size = self._format_size(size)

        user_prompt = PROMPT_OPTIMIZER_USER.format(
            theme=theme,
            styles=formatted_styles,
            size=formatted_size,
            purpose=purpose or "通用",
            extra_description=extra_description or "无"
        )

        # 调用 LLM
        optimized_prompt = await self._call_api(
            PROMPT_OPTIMIZER_SYSTEM,
            user_prompt
        )

        return optimized_prompt

    async def refine_prompt(
        self,
        original_prompt: str,
        refine_instruction: str
    ) -> str:
        """
        根据用户微调指令修改提示词

        Args:
            original_prompt: 原提示词
            refine_instruction: 用户微调指令

        Returns:
            修改后的提示词
        """
        user_prompt = REFINE_USER.format(
            original_prompt=original_prompt,
            refine_instruction=refine_instruction
        )

        refined_prompt = await self._call_api(
            REFINE_SYSTEM,
            user_prompt
        )

        return refined_prompt


# 全局服务实例
llm_service = LLMService()
