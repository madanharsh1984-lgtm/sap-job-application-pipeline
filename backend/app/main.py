from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import admin, auth, user
from app.core.settings import settings
from app.core.database import Base, engine, wait_for_database
from app.models import job, keyword_set, resume, user as user_model, user_keyword_map  # noqa: F401

@asynccontextmanager
async def lifespan(_app: FastAPI):
    wait_for_database()
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title='SAP Job Application SaaS MVP', lifespan=lifespan)

origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(',') if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/health')
def health():
    return {'status': 'ok'}


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(admin.router)
