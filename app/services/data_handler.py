import pandas as pd
import requests
import tkinter as tk
from tkinter import filedialog

def buscar_caminho_arquivo():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        title="Selecione um arquivo CSV",
        filetypes=(("Arquivo CSV", "*.csv"), ("Todos os arquivos", "*.*"))
    )

def limpar_e_formatar_dados(caminho_arquivo, colunas_pedidos):
    df = pd.read_csv(caminho_arquivo, encoding='latin1', sep=',')
    
    for coluna in colunas_pedidos:
        df[coluna] = df[coluna].astype(str).str.replace(',', '.', regex=False)
        df[coluna] = pd.to_numeric(df[coluna], errors='coerce')

    df = df.dropna(subset=colunas_pedidos)
    df['data'] = pd.to_datetime(df['data'])
    return df

def sincronizar_feriados(df):
    print("\nSincronizando feriados com a API...")
    anos_unicos = df['data'].dt.year.unique()
    lista_datas_feriados = []

    for ano in anos_unicos:
        url_api = f"https://brasilapi.com.br/api/feriados/v1/{ano}"
        try:
            resposta = requests.get(url_api, timeout=10)
            if resposta.status_code == 200:
                for feriado in resposta.json():
                    lista_datas_feriados.append(feriado['date'])
        except Exception as e:
            print(f"Aviso: Não foi possível baixar feriados de {ano}. Erro: {e}")

    datas_feriados_oficiais = pd.to_datetime(lista_datas_feriados)
    df['e_feriado'] = df['data'].isin(datas_feriados_oficiais).astype(int)
    print(f"{len(lista_datas_feriados)} feriados mapeados!")
    return df