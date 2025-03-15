import json

from fastapi import FastAPI
from controllers.geo_controller import router as geo_router
from controllers.route_controller import router as route_router
from fastapi.middleware.cors import CORSMiddleware
from services.geo_service import GeoService



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все домены (для разработки)
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, etc.)
    allow_headers=["*"],  # Разрешить все заголовки
)
# Подключаем роутер контроллера
app.include_router(geo_router, prefix="/api/geo")
app.include_router(route_router, prefix="/api/route")

f=open("static/json/codes.json", encoding="UTF-8")
config_data=json.load(f)
GeoService.set_config(config_data)


# Запуск приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)