import requests

headers = {
    'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImU2ZmQ1ZmUyLTQwNDQtNGFlZC05NjBmLWQ0ZTE4YjVmYzk0ZiIsImlhdCI6MTcxNjk4MDY4MCwic3ViIjoiZGV2ZWxvcGVyL2IwMjMzYjU1LTczMDgtMjU2My01YjE0LWI5ZGE0OTk1ZmM3MCIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjk1LjEyNy4xNTMuMjUzIl0sInR5cGUiOiJjbGllbnQifV19.-UPJECr3iSX3CcMC5L3bAi-xv41kSJsQrg9XfeWZHiWGHZERnzMz78gzCrWwXx7sIfo7k0KJIN9kUoQ-lvFXIA',  # Reemplaza 'tu_token_aqui' con tu token real
    'Accept': 'application/json'
}

def get_user(player_tag):
    url = f'https://api.clashofclans.com/v1/players/{player_tag}'
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

def get_clan(clan_tag):
    url = f'https://api.clashofclans.com/v1/clans/{clan_tag}'
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