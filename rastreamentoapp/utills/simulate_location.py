import random
import time

import requests

API_URL = "http://127.0.0.1:8000/api/v1/locations/"

TOKEN = """eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwi
ZXhwIjoxNzQ1ODk1NjUxLCJpYXQiOjE3NDU4OTUzNTEsImp0aSI6ImQxOGU5MjE3N2M4NjQ2NThiMzI
wMjg3ODZkNzQ5YmMxIiwidXNlcl9pZCI6MX0.7sk34HptplWtDDVjjh6tEE6JFjAk4sBBEqkZ3ZTjKTU"""

HEADERS = {"Authorization": f"Bearer {TOKEN}"}

VEHICLE_ID = "85de1fee-01d1-446e-8643-e64e02d31484"


def simulate_location():
    while True:
        data = {
            "vehicle": VEHICLE_ID,
            "latitude": round(-23.5 + random.random(), 6),
            "longitude": round(-46.6 + random.random(), 6),
            "speed": round(random.uniform(0, 80), 2),
        }
        response = requests.post(
            API_URL,
            json=data,
        )  # headers=HEADERS)
        print(response.status_code, response.json())
        time.sleep(5)  # envio a cada 2 segundos


def obter_posicoes():
    while True:
        url = f"http://127.0.0.1:8000/api/v1/vehicles/{VEHICLE_ID}/recent_locations/"
        response = requests.get(url, headers=HEADERS)

        for p in response.json():
            print("Últimas posições:", p)
            time.sleep(5)


if __name__ == "__main__":
    simulate_location()
    # obter_posicoes()
