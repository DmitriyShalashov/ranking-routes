import httpx


class RouteService:
    config=None

    @classmethod
    def set_config(cls, config):
        cls.config = config
    @staticmethod
    async def get_transfers_in_city(s1, s2):
        url="https://routing.api.2gis.com/public_transport/2.0"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url,
                                            params={
                                                "apikey": "76382da2-1f94-4102-afdd-9c4361a1e812",
                                                "source": s1,
                                                "target": s2,
                                                "start_time": date,
                                                "transport": [""]}
                                            )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                raise Exception(f"Ошибка внешнего API: {e}")

            except Exception as e:
                raise Exception(f"Произошла ошибка: {e}")
    @staticmethod
    async def get_route_by_from_to(frm="c22", to="c213", date="2025-04-15", transfers=True):
        url = "https://api.rasp.yandex.net/v3.0/search/"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url,
                                            params={
                                                "apikey": "76382da2-1f94-4102-afdd-9c4361a1e812",
                                                "from": frm,
                                                "to": to,
                                                "date": date,
                                                "transfers": transfers}
                                            )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                raise Exception(f"Ошибка внешнего API: {e}")

            except Exception as e:
                raise Exception(f"Произошла ошибка: {e}")
