from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.api import router as main_router


app = FastAPI(
    title='ChatBot Interface',
    version='0.0.1',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=["*"]
)

app.include_router(main_router)
