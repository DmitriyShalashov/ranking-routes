import httpx
import pandas as pd
class RecService:
    model = None

    @classmethod
    def set_model(cls, model):
        cls.model = model

    @staticmethod
    def get_score(time, cost):
        try:
            return RecService.model.predict(pd.DataFrame(data={"cost":[cost], "time":[time]}))[0]
        except httpx.HTTPStatusError as e:
            raise Exception(f"Ошибка внешнего API: {e}")
        except Exception as e:
            raise Exception(f"Произошла ошибка: {e}")