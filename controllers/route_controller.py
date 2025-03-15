import json

from fastapi import APIRouter, HTTPException
from services.route_service import RouteService
from services.geo_service import GeoService
import itertools
from datetime import datetime, timezone
import matplotlib.pyplot as plt

def get_available_transfer_duration(dt1, dt2):
    dt1_sec = datetime.fromisoformat(dt1).astimezone(timezone.utc).timestamp()
    dt2_sec = datetime.fromisoformat(dt2).astimezone(timezone.utc).timestamp()
    return dt2_sec - dt1_sec >= 4 * 60 * 60


def checkDebilizm(dt1, dt2):
    dt1_sec = datetime.fromisoformat(dt1).astimezone(timezone.utc).timestamp()
    dt2_sec = datetime.fromisoformat(dt2).astimezone(timezone.utc).timestamp()
    return dt2_sec - dt1_sec


router = APIRouter()


@router.get("/get_route")
async def get_route_by_stations(frm, to, date, transfers):
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
                directs.append([{
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

                }])
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
                for i in range(len(res_transfer) - 1):
                    if not get_available_transfer_duration(res_transfer[i]["arrival"],res_transfer[i + 1]["departure"]):
                        available = False
                        break
                if available:
                    grouped_transfers.append(res_transfer)
        mn=10**9
        filtered_transfers=[]
        for transfer in grouped_transfers:
            if checkDebilizm(transfer[0]["departure"], transfer[-1]["arrival"]) < mn:
                mn=checkDebilizm(transfer[0]["departure"], transfer[-1]["arrival"])
        for transfer in grouped_transfers:
            if checkDebilizm(transfer[0]["departure"], transfer[-1]["arrival"]) < 1.5 * mn:
                filtered_transfers.append(transfer)

        print(len(filtered_transfers))
        print(sum(len(transfer) for transfer in transfers))
        return json.dumps({"data": filtered_transfers})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
