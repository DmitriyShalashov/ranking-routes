import httpx

class GeoService:
    config = None

    @classmethod
    def set_config(cls, config):
        cls.config = config

    @staticmethod
    async def get_point_by_name(name="Москва"):
        url = "https://geocode-maps.yandex.ru/1.x"
        async with httpx.AsyncClient() as client:
            try:

                response = await client.get(url,
                                            params={
                                                "apikey":"d4ef20e7-faca-4571-bc6c-bd912c9142e8",
                                                "geocode":name,
                                                "lang":"ru_RU",
                                                "format":"json",
                                                "kind":"locality"

                })
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                raise Exception(f"Ошибка внешнего API: {e}")
            except Exception as e:
                raise Exception(f"Произошла ошибка: {e}")

    @staticmethod
    async def get_code_by_cords(lat=55.755864,lng=37.617698):
        url = "https://api.rasp.yandex.net/v3.0/nearest_settlement/"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url,
                                            params={
                                                "apikey":"76382da2-1f94-4102-afdd-9c4361a1e812",
                                                "lat":lat,
                                                "lng":lng,
                                                "distance":10
                                            })
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                raise Exception(f"Ошибка внешнего API: {e}")
            except Exception as e:
                raise Exception(f"Произошла ошибка: {e}")

    @staticmethod
    def get_city_by_station(station):
        return GeoService.config[station]