from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class RunConfig(BaseModel):
    host: str
    port: int
    log_level: str
    reload: bool = False
    workers: int


class ApiPrefix(BaseModel):
    api_prefix: str = "/api"
    fruits_prefix: str = "/fruits"


class ApiConfig(BaseModel):
    prefix: ApiPrefix = ApiPrefix()
    create_custom_doc_urls: bool = True
    use_gzip: bool
    version: str = "1.1.2"
    title: str = "Fruits CRUD"
    description: str = """
Is an application that implements CRUD (create, read, update, delete) operations on fruits.

Useful information:
- If the response size exceeds 1500 bytes, the data is compressed using GZIP;
- When performing partial update operations, if you want to leave the field unchanged, then leave the field value set to false. 
"""


class CDNConfig(BaseModel):
    swagger_js_url: str = "https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"
    swagger_css_url: str = "https://unpkg.com/swagger-ui-dist@5/swagger-ui.css"
    redoc_js_url: str = "https://unpkg.com/redoc@next/bundles/redoc.standalone.js"


class DatabaseConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str
    name: str

    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @property
    def get_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class CacheConfig(BaseModel):
    host: str
    port: int
    exp_seconds: int

    @property
    def get_url(self) -> str:
        return f"redis://{self.host}:{self.port}"


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )

    run: RunConfig
    api: ApiConfig
    cdn: CDNConfig = CDNConfig()
    database: DatabaseConfig
    cache: CacheConfig


settings = Settings()
