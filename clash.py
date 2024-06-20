import requests
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Token de autorización y encabezados
headers = {
    'Authorization': f'Bearer {os.getenv("CLASH_API_TOKEN")}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def get_user(player_tag):
    encoded_player_tag = player_tag.replace('#', '%23')
    url = f'https://api.clashofclans.com/v1/players/{encoded_player_tag}'
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 403:
            raise Exception("Error 403: Acceso prohibido. Verifica tu token de autorización y las IPs permitidas.")
        else:
            raise Exception(f"HTTP error occurred: {http_err}")
    except Exception as err:
        raise Exception(f"Other error occurred: {err}")

def get_clan(clan_tag):
    encoded_clan_tag = clan_tag.replace('#', '%23')
    url = f'https://api.clashofclans.com/v1/clans/{encoded_clan_tag}'
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 403:
            raise Exception("Error 403: Acceso prohibido. Verifica tu token de autorización y las IPs permitidas.")
        else:
            raise Exception(f"HTTP error occurred: {http_err}")
    except Exception as err:
        raise Exception(f"Other error occurred: {err}")

def search_clans(clan_name):
    url = f'https://api.clashofclans.com/v1/clans?name={clan_name}'
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()['items']
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 403:
            raise Exception("Error 403: Acceso prohibido. Verifica tu token de autorización y las IPs permitidas.")
        else:
            raise Exception(f"HTTP error occurred: {http_err}")
    except Exception as err:
        raise Exception(f"Other error occurred: {err}")
