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

def remover_outliers(df, coluna):
    """
    Remove outliers de um DataFrame usando o método do Intervalo Interquartil (IQR).
    """
    # Calcula o primeiro e o terceiro quartil (25% e 75% dos dados)
    Q1 = df[coluna].quantile(0.25)
    Q3 = df[coluna].quantile(0.75)
    
    # Calcula o IQR
    IQR = Q3 - Q1
    
    # Define os limites de corte
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR
    
    # Filtra o DataFrame mantendo apenas o que está dentro dos limites saudáveis
    df_limpo = df[(df[coluna] >= limite_inferior) & (df[coluna] <= limite_superior)].copy()
    
    # Print informativo para você saber quantos dados foram jogados fora
    outliers_removidos = len(df) - len(df_limpo)
    print(f"Limpeza: {outliers_removidos} outliers removidos da coluna '{coluna}'.")
    
    return df_limpo