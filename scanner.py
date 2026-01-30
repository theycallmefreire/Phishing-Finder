import pandas as pd
import whois
from urllib.parse import urlparse

def procurar_url(caminho_arquivo, url_para_buscar):
    df = pd.read_csv(caminho_arquivo)
    filtro = df[df['url'] == url_para_buscar]  

    dados_phish = None
    if not filtro.empty:
        dados_phish = filtro.iloc[0].to_dict()

    dados_whois = None
    try:
        dominio = urlparse(url_para_buscar).netloc
        if dominio:
            w = whois.whois(dominio)
            dados_whois = {
                "criacao": str(w.creation_date),
                "expiracao": w.expiration_date,
                "registrador": w.registrar,
                "pais": w.country
            }
    except Exception as e:
        print(f"Erro ao buscar WHOIS: {e}")

    return {"Phishing_Finder": dados_phish, "whois": dados_whois}