"""
豆包 SeeDream 生图服务
"""

import httpx
import hashlib
import hmac
import json
from datetime import datetime, timezone
from typing import Optional
from app.core.config import settings
from app.core.styles import SIZE_OPTIONS


class ImageService:
    """豆包生图服务类"""

    def __init__(self):
        self.api_key = settings.doubao_api_key
        self.base_url = settings.doubao_base_url
        self.model = "doubao-seedream-3-0-t2i-250415"

    def _get_size_dimensions(self, size_id: str) -> tuple:
        """获取尺寸的宽高"""
        size_info = SIZE_OPTIONS.get(size_id, SIZE_OPTIONS["square_medium"])
        size_str = size_info.get("size", "1024x1024")
        width, height = size_str.split("x")
        return int(width), int(height)

    async def generate_image(
        self,
        prompt: str,
        size: str = "square_medium",
        style_strength: float = 0.8,
        seed: Optional[int] = None
    ) -> dict:
        """
        调用豆包 SeeDream API 生成图片

        Args:
            prompt: 优化后的提示词
            size: 尺寸ID
            style_strength: 风格强度 (0.1-1.0)
            seed: 随机种子（可选，用于复现）

        Returns:
            包含图片URL和元信息的字典
        """
        width, height = self._get_size_dimensions(size)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "prompt": prompt,
            "width": width,
            "height": height,
            "scale": style_strength * 10,  # 转换为 1-10 的范围
            "seed": seed or -1,  # -1 表示随机
            "response_format": "url"
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self.base_url}/v1/images/generations",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            result = response.json()

            # 解析响应
            image_data = result.get("data", [{}])[0]
            return {
                "image_url": image_data.get("url", ""),
                "revised_prompt": image_data.get("revised_prompt", prompt),
                "seed": result.get("seed"),
                "model": self.model
            }

    async def generate_image_with_retry(
        self,
        prompt: str,
        size: str = "square_medium",
        style_strength: float = 0.8,
        max_retries: int = 3
    ) -> dict:
        """
        带重试机制的图片生成

        Args:
            prompt: 优化后的提示词
            size: 尺寸ID
            style_strength: 风格强度
            max_retries: 最大重试次数

        Returns:
            生成结果
        """
        last_error = None

        for attempt in range(max_retries):
            try:
                result = await self.generate_image(
                    prompt=prompt,
                    size=size,
                    style_strength=style_strength
                )
                return result
            except httpx.HTTPStatusError as e:
                last_error = e
                if e.response.status_code >= 500:
                    # 服务端错误，重试
                    continue
                else:
                    # 客户端错误，直接抛出
                    raise
            except httpx.TimeoutException as e:
                last_error = e
                continue

        raise last_error or Exception("生成失败，已达最大重试次数")


# 全局服务实例
image_service = ImageService()
