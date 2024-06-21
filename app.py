import requests
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Token de autorización y encabezados
headers = {
    'Authorization': f'Bearer {os.getenv("CLASH_API_TOKEN")}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

app = Flask(__name__)

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
        return response.json().get('items', [])
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 403:
            raise Exception("Error 403: Acceso prohibido. Verifica tu token de autorización y las IPs permitidas.")
        else:
            raise Exception(f"HTTP error occurred: {http_err}")
    except Exception as err:
        raise Exception(f"Other error occurred: {err}")

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/search', methods=['POST'])
def search():
    search_type = request.form['type']
    search_term = request.form['term']
    try:
        if search_type == 'player':
            return redirect(url_for('detalle_jugador', player_tag=search_term))
        elif search_type == 'clan':
            return redirect(url_for('resultado_clan', clan_name=search_term))
    except Exception as e:
        error = str(e)
        return render_template('inicio.html', error=error)

@app.route('/resultado_clan/<clan_name>')
def resultado_clan(clan_name):
    try:
        clanes = search_clans(clan_name)
        return render_template('resultado_clan.html', clanes=clanes)
    except Exception as e:
        return render_template('inicio.html', error=str(e))

@app.route('/detallejugador/<player_tag>')
def detalle_jugador(player_tag):
    try:
        jugador = get_user(player_tag)
        return render_template('detallejugador.html', jugador=jugador)
    except Exception as e:
        return render_template('jugadores.html', error=str(e))

@app.route('/detalleclan/<clan_tag>')
def detalle_clan(clan_tag):
    try:
        clan = get_clan(clan_tag)
        return render_template('detalleclan.html', clan=clan)
    except Exception as e:
        return render_template('clanes.html', error=str(e))

@app.route('/jugadores/<clan_tag>')
def lista_jugadores(clan_tag):
    try:
        clan = get_clan(clan_tag)
        jugadores = clan.get('memberList', [])
        return render_template('lista_jugadores.html', jugadores=jugadores, clan_name=clan['name'])
    except Exception as e:
        return render_template('clanes.html', error=str(e))

@app.route('/extra_info/<player_tag>')
def extra_info(player_tag):
    try:
        jugador = get_user(player_tag)
        # Aquí puedes procesar y extraer la información adicional que necesites
        extra_info = {
            "heroes": jugador.get("heroes", []),
            "spells": jugador.get("spells", []),
            "troops": jugador.get("troops", [])
        }
        return render_template('extra_info.html', extra_info=extra_info, jugador_name=jugador['name'])
    except Exception as e:
        return render_template('inicio.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
