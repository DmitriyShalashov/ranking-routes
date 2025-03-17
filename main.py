import json

from fastapi import FastAPI
from controllers.geo_controller import router as geo_router
from controllers.route_controller import router as route_router
from fastapi.middleware.cors import CORSMiddleware
from services.geo_service import GeoService
from services.rec_service import RecService
from services.route_service import RouteService


import lightgbm as lgb
import numpy as np


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

f = open("static/json/routes.json", encoding="UTF-8")
config_data = json.load(f)
RouteService.set_config(config_data)

model = lgb.Booster(model_file="static/weights/model.txt")
RecService.set_model(model)
print(RecService.get_score(-14000,-21000))
print(RecService.get_score(-20000,-13000))
print(RecService.get_score(-51000,-15000))
print(RecService.get_score(-34000,-10000))
# Запуск приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)