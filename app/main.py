from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.models.schemas import ChatRequest, ChatResponse, HealthResponse
from app.services.catalog import load_catalog
from app.services.recommender import ChatRecommender
from app.services.retrieval import load_vector_index


def create_app() -> FastAPI:
    app = FastAPI(title="SHL Assessment Recommender")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    async def startup() -> None:
        catalog = load_catalog(settings.CATALOG_PATH)
        vector_index = load_vector_index(settings.INDEX_PATH)
        app.state.recommender = ChatRecommender(catalog, vector_index)

    @app.get("/health", response_model=HealthResponse)
    async def health() -> HealthResponse:
        return HealthResponse()

    @app.post("/chat", response_model=ChatResponse)
    async def chat(request: ChatRequest) -> ChatResponse:
        recommender = getattr(app.state, "recommender", None)
        if recommender is None:
            raise HTTPException(status_code=503, detail="Service not ready.")
        try:
            return recommender.handle_chat(request)
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    return app


app = create_app()
