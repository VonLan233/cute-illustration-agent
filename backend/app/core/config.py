from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # DeepSeek API 配置
    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com/v1"

    # 豆包生图 API 配置
    doubao_api_key: str = ""
    doubao_base_url: str = "https://visual.volcengineapi.com"

    # 数据库配置
    database_url: Optional[str] = None

    # 服务配置
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
