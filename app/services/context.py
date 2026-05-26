import sqlite3
import pandas as pd
import requests
from datetime import datetime, timedelta
from core.config import settings

def buscar_vendas_passadas(produto:str,data_alvo:datetime) -> float:
    inicio_semana_passada = data_alvo - timedelta(days=data_alvo.weekday() + 7)
    fim_semana_passada = inicio_semana_passada + timedelta(days=6)

    inicio_str = inicio_semana_passada.strftime("%Y-%m-%d")
    fim_str = fim_semana_passada.strftime("%Y-%m-%d")

    conexao = sqlite3.connect(settings.DB_PATH)
    cursor = conexao.cursor()

    query = """
        SELECT SUM(qtd) FROM historico_vendas 
        WHERE produto = ? AND data >= ? AND data <= ?
    """
    cursor.execute(query, (produto, inicio_str, fim_str))
    resultado = cursor.fetchone()[0]
    conexao.close()

    return float(resultado) if resultado else 0.0

def construir_dados_completos(produto: str, data_str:str) -> dict:
    data_alvo = pd.to_datetime(data_str)
    
    mes = data_alvo.month
    semana_do_ano = data_alvo.isocalendar()[1]

    vendas_passadas = buscar_vendas_passadas(produto, data_alvo)

    tem_feriado = 0
    ano = data_alvo.year
    try:
        resp_feriados = requests.get(f"https://brasilapi.com.br/api/feriados/v1/{ano}")
        if resp_feriados.status_code == 200:
            datas_feriados = [f['date'] for f in resp_feriados.json()]
            if data_str in datas_feriados:
                tem_feriado = 1
    except:
        pass

    lat,lon = -23.09, -47.22#TODO: Definir cordenadas com base na loja
    url_clima = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,relative_humidity_2m_mean&timezone=America%2FSao_Paulo&start_date={data_str}&end_date={data_str}"

    try:
        resp_clima = requests.get(url_clima, timeout=5).json()
        temp_max = resp_clima['daily']['temperature_2m_max'][0]
        temp_min = resp_clima['daily']['temperature_2m_min'][0]
        temp_media = (temp_max + temp_min) / 2
        umidade = resp_clima['daily']['relative_humidity_2m_mean'][0]
    except:
        temp_max, temp_min, temp_media, umidade = 28.0, 18.0, 23.0, 60.0

    return {
        "produto": produto,
        "temp_min_semana": temp_min,
        "temp_max_semana": temp_max,
        "temp_media_semana": temp_media,
        "umidade_media_semana": umidade,
        "tem_feriado_na_semana": tem_feriado,
        "vendas_semana_passada": vendas_passadas,
        "mes": mes,
        "semana_do_ano": semana_do_ano
    }