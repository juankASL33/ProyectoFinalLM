import requests
from flask import Flask, render_template, request, redirect, url_for

# Token de autorización y encabezados
headers = {
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImM4NThmODVlLWZlYmUtNDIzYi04ZjRkLTRkMjZhODA5NGFjNSIsImlhdCI6MTcxODM1MjgzMSwic3ViIjoiZGV2ZWxvcGVyL2M1ZWMzNDUzLTIwOWMtODYxOS1lOGY5LWQyZDI2N2M1OWFmMyIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjgwLjMxLjcxLjE0MiJdLCJ0eXBlIjoiY2xpZW50In1dfQ.x5G7LfJYIBDBpxSDChhck3A3egQYqJd5Ng8XtTJifTV5cOY75cjTrcE8jqjTTlK9CUQa049irIyz_JVe3_tWhg',
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
            results = search_clans(search_term)
            return render_template('clanes.html', clanes=results)
    except Exception as e:
        error = str(e)
        return render_template('clanes.html', clanes=[], error=error)

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


if __name__ == '__main__':
    app.run(debug=True)
