from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    CATALOG_PATH: str = str(BASE_DIR / "data" / "catalog.json")
    INDEX_PATH: str = str(BASE_DIR / "data" / "index.pkl")
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    MAX_TURNS: int = 8
    MAX_RECOMMENDATIONS: int = 10
    DEFAULT_RECOMMENDATION_COUNT: int = 5
    TOP_K: int = 20
    REQUEST_TIMEOUT_SECONDS: int = 25
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175",
        "https://shl-assessment-recommender-git-main-gitansh01s-projects.vercel.app",
        "https://shl-assessment-recommender-5joh.onrender.com",
    ]
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
