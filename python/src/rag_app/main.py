from __future__ import annotations

from fastapi import FastAPI

from rag_app.api.routes import router


app = FastAPI(title="RAG Interview Python")
app.include_router(router)

