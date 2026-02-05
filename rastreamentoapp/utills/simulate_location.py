import random
import time

import requests


API_URL = "http://127.0.0.1:8000/api/v1/locations/"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ1ODk1NjUxLCJpYXQiOjE3NDU4OTUzNTEsImp0aSI6ImQxOGU5MjE3N2M4NjQ2NThiMzIwMjg3ODZkNzQ5YmMxIiwidXNlcl9pZCI6MX0.7sk34HptplWtDDVjjh6tEE6JFjAk4sBBEqkZ3ZTjKTU"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

VEHICLE_ID = "9c1fa0c6-cda4-4d0d-a70a-2ce3e8115822"


def enviar_localizacao():
    while True:
        data = {
            "vehicle": VEHICLE_ID,
            "latitude": round(-23.5 + random.random(), 6),
            "longitude": round(-46.6 + random.random(), 6),
            "speed": round(random.uniform(0, 80), 2),
        }
        response = requests.post(API_URL, json=data, headers=HEADERS)
        print(response.status_code, response.json())
        time.sleep(5)  # simula envio a cada 5 segundos


def obter_posicoes():
    while True:
        url = f"http://127.0.0.1:8000/api/v1/vehicles/{VEHICLE_ID}/recent_locations/"
        response = requests.get(url, headers=HEADERS)

        for p in response.json():
            print("Últimas posições:", p)
            time.sleep(5)

        # print("Últimas posições:", response.json())
        # time.sleep(10)  # simula atualização de mapa a cada 10 segundos


if __name__ == "__main__":
    enviar_localizacao()
    # obter_posicoes()