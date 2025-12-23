from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from utils.database import engine, Base
from routes import (
    categories_router,
    products_router,
    auth_router,
    orders_router
)

# Создание таблиц в БД
Base.metadata.create_all(bind=engine)

# Создание приложения FastAPI
app = FastAPI(
    title="Магазин Одежды API",
    description="REST API для онлайн-магазина одежды",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(auth_router)
app.include_router(categories_router)
app.include_router(products_router)
app.include_router(orders_router)


@app.get("/", tags=["Общее"])
def root():
    """Корневой эндпоинт"""
    return {
        "message": "Добро пожаловать в API Магазина Одежды",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["Общее"])
def health_check():
    """Проверка здоровья API"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
