# в файле достаем переменные из consul. Для доступа к consul используем переменные из .env
from dotenv import load_dotenv
import os
import consul
import yaml
from functools import lru_cache
from pydantic import BaseModel
from typing import Dict, Any

load_dotenv()

CONSUL_HOST = os.getenv("CONSUL_HOST", "localhost")
CONSUL_PORT = int(os.getenv("CONSUL_PORT", 8500))
CONSUL_SCHEME = os.getenv("CONSUL_SCHEME", "http")
CONSUL_PREFIX = os.getenv("CONSUL_PREFIX")
CONSUL_ACCESS_READ = os.getenv("CONSUL_ACCESS_READ")


class RedisConfig(BaseModel):
    url: str


class RabbitMQConfig(BaseModel):
    url: str
    user: str
    password: str


class Settings(BaseModel):
    redis: RedisConfig
    rabbitmq: RabbitMQConfig


@lru_cache
def load_settings() -> Settings:
    client = consul.Consul(
        host=CONSUL_HOST,
        port=CONSUL_PORT,
        scheme=CONSUL_SCHEME,
        token=CONSUL_ACCESS_READ,
        verify=False,
    )

    index, data = client.kv.get(f"{CONSUL_PREFIX}/data")
    if not data or "Value" not in data:
        raise RuntimeError("Missing config key: data")

    raw_yaml = data["Value"].decode("utf-8")
    config_dict = yaml.safe_load(raw_yaml)

    return Settings.model_validate(config_dict)


settings = load_settings()
