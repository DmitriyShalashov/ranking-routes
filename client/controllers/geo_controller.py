from fastapi import APIRouter, HTTPException
from services.geo_service import GeoService
import json


router = APIRouter()

@router.get("/geo_point")
async def get_external_data(name):
    if not name:
        return json.dumps({"data":[]})
    try:
        result=[]
        data = await GeoService.get_point_by_name(name)
        for geo_obj in data["response"]["GeoObjectCollection"]["featureMember"]:
            type=geo_obj["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["kind"]
            if type=="locality" or type=="province":
                print("Пункт: ",geo_obj["GeoObject"]["name"],geo_obj["GeoObject"]["description"])
                cords=list(map(float,geo_obj["GeoObject"]["Point"]["pos"].split(" ")))
                print("Координаты: ","lat: ",cords[1]," lng: ",cords[0])
                result.append({
                    "lat": cords[1],
                    "lng": cords[0],
                    "name":geo_obj["GeoObject"]["name"],
                    "description": geo_obj["GeoObject"]["description"],
                })
        # 0 - lng 1 - lat
        print(result)
        return json.dumps({"data":result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_code_city")
async def get_city_code(name):
    try:
        data = await GeoService.get_code_by_cords(name)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_city_by_station")
async def get_city_code_by_station(station):
    try:
        data = GeoService.get_city_by_station(station)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))