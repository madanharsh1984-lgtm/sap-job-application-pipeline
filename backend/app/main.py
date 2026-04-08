from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import admin, auth, user
from app.core.config import settings
from app.core.database import Base, engine
from app.models import job, resume, user as user_model  # noqa: F401

app = FastAPI(title='SAP Job Application SaaS MVP')

origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(',') if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event('startup')
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get('/health')
def health():
    return {'status': 'ok'}


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(admin.router)
