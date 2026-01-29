from flask import Flask, render_template, request
from scanner import procurar_url
import os
import requests

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
CSV_PATH = os.path.join(DATA_DIR, "verified_online.csv")

def garantir_csv():
    # Cria a pasta 'data' caso ela não exista
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"Pasta criada: {DATA_DIR}")

    if not os.path.exists(CSV_PATH):
        url_download = "http://data.phishtank.com/data/online-valid.csv"
        
        headers = {'User-Agent': 'PhishGuard-App-Guilherme'}
        try:
            response = requests.get(url_download, headers=headers, timeout=30)
            response.raise_for_status() 
            
            with open(CSV_PATH, 'wb') as f:
                f.write(response.content)
        except Exception as e:
            print(f"Erro ao baixar CSV: {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    url_pesquisada = None

    if request.method == 'POST':
        url_pesquisada = request.form.get('url')
        if os.path.exists(CSV_PATH):
            resultado = procurar_url(CSV_PATH, url_pesquisada)
        else:
            resultado = "Erro: Base de dados indisponível."
    
    return render_template('index.html', resultado=resultado, url=url_pesquisada)

if __name__ == '__main__':
    garantir_csv()
    app.run(debug=True)