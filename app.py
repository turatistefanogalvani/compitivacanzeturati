from flask import Flask, render_template, redirect, url_for
import pandas as pd
import random

app = Flask(__name__)

dati_pokemon = pd.read_csv('pokemon.csv')
credito_giocatore = 100
raccolta = []

distribuzione_rarita = ['Comune'] * 70 + ['Non Comune'] * 20 + ['Rara'] * 9 + ['Ultra Rara'] * 1

def genera_pacchetto():
    bustina = []
    credito_bonus = 0
    carte_estratte = 0
    while carte_estratte < 5:
        rarita_estratta = random.choice(distribuzione_rarita)
        carte_possibili = dati_pokemon[dati_pokemon['Rarità'] == rarita_estratta]
        if len(carte_possibili) > 0:
            carta_scelta = carte_possibili.iloc[random.randint(0, len(carte_possibili) - 1)]
            bustina.append(carta_scelta.to_dict())
            if rarita_estratta == 'Comune':
                credito_bonus += 1
            elif rarita_estratta == 'Non Comune':
                credito_bonus += 5
            elif rarita_estratta == 'Rara':
                credito_bonus += 10
            elif rarita_estratta == 'Ultra Rara':
                credito_bonus += 20
            carte_estratte += 1
    return bustina, credito_bonus

def salva_raccolta():
    raccolta_df = pd.DataFrame(raccolta)
    raccolta_df.to_csv('collezione.csv', index=False)

def carica_raccolta():
    global raccolta
    try:
        raccolta = pd.read_csv('collezione.csv').to_dict(orient='records')
    except FileNotFoundError:
        raccolta = []

carica_raccolta()

@app.route('/')
def pagina_principale():
    return render_template('index.html', credito_giocatore=credito_giocatore, raccolta=raccolta)

@app.route('/genera_pacchetto', methods=['POST'])
def genera_pacchetto_route():
    global credito_giocatore, raccolta
    if credito_giocatore >= 10:
        credito_giocatore -= 10
        bustina, credito_bonus = genera_pacchetto()
        raccolta.extend(bustina)
        salva_raccolta()
        credito_giocatore += credito_bonus
    return redirect(url_for('pagina_principale'))

@app.route('/visualizza_raccolta', methods=['GET'])
def visualizza_raccolta_route():
    return render_template('collezione.html', raccolta=raccolta)

@app.route('/visualizza_credito', methods=['GET'])
def visualizza_credito_route():
    return render_template('punti.html', credito_giocatore=credito_giocatore)

if __name__ == '__main__':
    app.run(debug=True)
