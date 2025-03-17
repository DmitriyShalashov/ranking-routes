import json

from fastapi import APIRouter, HTTPException, Body
from services.route_service import RouteService
from services.geo_service import GeoService
import itertools
from datetime import datetime, timezone
from services.rec_service import RecService
import matplotlib.pyplot as plt

def get_price(transport,duration,city_from,city_to):
    coef_transport = 1.3
    if transport == "train":
        coef_transport = 0.8 if duration >= 3600 * 6 else 1.2
    elif transport == "plane":
        coef_transport = 3.7
    elif transport == "suburban":
        coef_transport = 1.1
    elif transport == "bus":
        coef_transport = 0.75

    coef_city = 1
    if city_to in ["Москва", "Новосибирск", "Санкт-Петербург", "Краснодар"]:
        coef_city += 0.1
    if city_from in ["Москва", "Новосибирск", "Санкт-Петербург", "Краснодар"]:
        coef_city += 0.1
    price_per_sec = 0.15
    return duration * price_per_sec * coef_city * coef_transport ** (max(duration // (3600 * 4), 1.2))
def get_available_transfer_duration(frm, to):
    station_from = frm["to"]
    date_from = frm["arrival"]
    transport_type_from = frm["transport"]
    station_to = to["from"]
    date_to = to["departure"]
    transport_type_to = to["transport"]

    minimal_transfer_time = 0
    if station_to["station_code"] == station_from["station_code"]:  # Если пересадка в рамках одной станции
        if transport_type_from == "plane":  # Пересадка в аэропорту
            minimal_transfer_time = 2 * 3600
        elif transport_type_from == "train":  # Время на смену поезда и навигацию внутри вокзала
            minimal_transfer_time = 1 * 3600
        elif transport_type_from == "bus":  # Время на навигацию внутри автовокзала
            minimal_transfer_time = 0.75 * 3600
        elif transport_type_from == "suburban":  # Время на пересадку с одной пригородной электрички на другую
            minimal_transfer_time = 3600 // 4
        else:
            minimal_transfer_time = 1.5 * 3600  # Время на пересадку на других видах транспорта
    else:
        # Учет времени на перемещение между станциями
        if station_from["city_title"] == "Москва" or station_from["city_title"] == "Санкт-Петербург":
            # Учет специфики пересадок между станциями внутри Санкт-Петербурга и Москвы
            filename = f"{station_to['station_title']}-{station_from['station_title']}"
            if filename in RouteService.config.keys():
                minimal_transfer_time += RouteService.config[filename]['duration']
            else:
                minimal_transfer_time += 2 * 3600  # Среднее время на перемещение по городу между станциями
        else:
            minimal_transfer_time += 2 * 3600  # Среднее время на перемещение по городу между станциями

        # Учет времени посадки с учетом специфики станций
        if transport_type_to == "plane":
            minimal_transfer_time += 2 * 3600
        elif transport_type_to == "train":
            minimal_transfer_time += 1 * 3600
        elif transport_type_to == "bus":
            minimal_transfer_time += 0.5 * 3600
        elif transport_type_to == "suburban":
            minimal_transfer_time += 0.25 * 3600
        else:  # Учет времени на посадку на иные виды транспорта (паром, вертолет, корабль)
            minimal_transfer_time += 1 * 3600

        # Учет времени на выход с вокзала/станции
        if transport_type_to == "plane":
            minimal_transfer_time += 1 * 3600
        elif transport_type_to == "train":
            minimal_transfer_time += 0.25 * 3600
        elif transport_type_to == "bus":
            minimal_transfer_time += 3600 // 10
        elif transport_type_to == "suburban":
            minimal_transfer_time += 3600 // 10
        else:  # Учет времени на посадку на иные виды транспорта (паром, вертолет, корабль)
            minimal_transfer_time += 0.5 * 3600

    dt1_sec = datetime.fromisoformat(date_from).astimezone(timezone.utc).timestamp()
    dt2_sec = datetime.fromisoformat(date_to).astimezone(timezone.utc).timestamp()

    return dt2_sec - dt1_sec >= minimal_transfer_time


def get_full_transfer_path(frm, to):
    if frm["to"]["city_title"] == "Москва" or to["from"]["city_title"] == "Санкт-Петербург":
        filename = f"{to["from"]['station_title']}-{frm["to"]['station_title']}"
        if filename in RouteService.config.keys():
            return RouteService.config[filename]["details"]
    return []


def check(dt1, dt2):
    dt1_sec = datetime.fromisoformat(dt1).astimezone(timezone.utc).timestamp()
    dt2_sec = datetime.fromisoformat(dt2).astimezone(timezone.utc).timestamp()
    return dt2_sec - dt1_sec


router = APIRouter()


@router.post("/get_route/")
async def get_route_by_stations(body=Body()):
    print(body["to"])
    transfers = body["transfers"]
    date = body["date"]
    frm = await GeoService.get_code_by_cords(lng=body["frm"]["lng"], lat=body["frm"]["lat"])
    to = await GeoService.get_code_by_cords(lng=body["to"]["lng"], lat=body["to"]["lat"])
    frm = frm["code"]
    to = to["code"]
    try:
        data = await RouteService.get_route_by_from_to(frm, to, date, transfers)
        transfers = []
        directs = []
        for segment in data["segments"]:
            if segment["has_transfers"]:
                transfers.append([])

                for routes in segment["details"]:
                    if "thread" in routes:
                        transfers[-1].append({
                            "from": {
                                "station_code": segment["departure_from"]["code"],
                                "city_code": routes["from"]["code"],
                                "city_title": routes["from"]["title"],
                                "station_title": segment["departure_from"]["title"],
                            },
                            "to": {
                                "station_code": segment["arrival_to"]["code"],
                                "city_code": routes["to"]["code"],
                                "city_title": routes["to"]["title"],
                                "station_title": segment["arrival_to"]["title"],
                            },
                            "start_date": routes["start_date"],
                            "departure": routes["departure"],
                            "transport": routes["thread"]["transport_type"],
                            "duration": routes["duration"],
                            "arrival": routes["arrival"],
                        })
            else:
                directs.append([{"route": {
                    "from": {
                        "city_code": data["search"]["from"]["code"],
                        "station_code": segment["from"]["code"],
                        "station_title": segment["from"]["title"],
                        "city_title": data["search"]["from"]["title"]
                    },
                    "to": {
                        "city_code": data["search"]["to"]["code"],
                        "station_code": segment["to"]["code"],
                        "station_title": segment["to"]["title"],
                        "city_title": data["search"]["to"]["title"]
                    },
                    "start_date": date,
                    "departure": segment["departure"],
                    "transport": segment["thread"]["transport_type"],
                    "duration": segment["duration"],
                    "arrival": segment["arrival"],

                }, "is_transfer": False}])
        detailed_transfers = []
        city_set = set()
        for transfer in transfers:
            detailed_transfers.append([])
            for route in transfer:
                if route["from"]["city_code"] + route["to"]["city_code"] in city_set:
                    continue
                details = []
                city_set.add(route["from"]["city_code"] + route["to"]["city_code"])

                data = await RouteService.get_route_by_from_to(frm=route["from"]["city_code"],
                                                               to=route["to"]["city_code"],
                                                               date=route["start_date"],
                                                               transfers=False)
                for segment in data["segments"]:
                    if segment["has_transfers"]:
                        pass
                    else:
                        details.append({
                            "from": {
                                "city_code": data["search"]["from"]["code"],
                                "station_code": segment["from"]["code"],
                                "station_title": segment["from"]["title"],
                                "city_title": data["search"]["from"]["title"]
                            },
                            "to": {
                                "city_code": data["search"]["to"]["code"],
                                "station_code": segment["to"]["code"],
                                "station_title": segment["to"]["title"],
                                "city_title": data["search"]["to"]["title"]
                            },
                            "start_date": date,
                            "departure": segment["departure"],
                            "transport": segment["thread"]["transport_type"],
                            "duration": segment["duration"],
                            "arrival": segment["arrival"],
                        })
                detailed_transfers[-1].append(details)

        grouped_transfers = []
        for transfer in detailed_transfers:
            if len(transfer) == 0:
                continue
            decart = itertools.product(*transfer)
            for prod in decart:
                res_transfer = list(prod)
                available = True
                crosses = []
                for i in range(len(res_transfer) - 1):
                    if not get_available_transfer_duration(res_transfer[i], res_transfer[i + 1]):
                        available = False
                        break

                if available:
                    grouped_transfers.append([])
                    for i in range(len(res_transfer) - 1):
                        crosses = get_full_transfer_path(res_transfer[i], res_transfer[i + 1])
                        grouped_transfers[-1].append({"is_transfer": False, "route": res_transfer[i]})
                        if crosses:
                            grouped_transfers[-1].append({"is_transfer": True, "details": crosses})
                        else:
                            dt1t=datetime.fromisoformat(res_transfer[i+1]["departure"]).astimezone(timezone.utc).timestamp()
                            dt2t = datetime.fromisoformat(res_transfer[i]["arrival"]).astimezone(timezone.utc).timestamp()
                            grouped_transfers[-1].append({"is_transfer": True,
                                                          "details": [{
                                                              "from": None,
                                                              "to": None,
                                                              "transport_type": "pedestrian",
                                                              "duration":dt1t - dt2t
                                                          }]})
                    grouped_transfers[-1].append({"is_transfer": False, "route": res_transfer[-1]})
        mn = 10 ** 9
        filtered_transfers = []
        for transfer in grouped_transfers:
            if check(transfer[0]["route"]["departure"], transfer[-1]["route"]["arrival"]) < mn:
                mn = check(transfer[0]["route"]["departure"], transfer[-1]["route"]["arrival"])
        for transfer in grouped_transfers:
            if check(transfer[0]["route"]["departure"], transfer[-1]["route"]["arrival"]) < 1.75 * mn:
                filtered_transfers.append(transfer)

        result_transfers=[]
        for transfer in grouped_transfers+directs:
            duration=check(transfer[0]["route"]["departure"], transfer[-1]["route"]["arrival"])
            price=0
            for sub_transfer in transfer:
                if not sub_transfer["is_transfer"]:
                    price+=get_price(
                        transport=sub_transfer["route"]["transport"],
                        duration=duration,
                        city_from=sub_transfer["route"]["from"]["city_title"],
                        city_to=sub_transfer["route"]["to"]["city_title"]
                    )
            score=RecService.get_score(cost=price, time=duration)
            result_transfers.append({
                "info":transfer,
                "score":score,
                "duration":duration,
                "price":price
            })

        print(len(filtered_transfers))
        print(sum(len(transfer) for transfer in transfers))
        #return json.dumps({"data": filtered_transfers + directs})
        return result_transfers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
