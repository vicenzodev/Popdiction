import glob
import os
import joblib
import pandas as pd
from core.config import settings
from ml.trainer import treinamento_automatico

class ModeloPrevisao:
    def __init__(self):
        self.modelos = {}
        self.carregar_todos_modelos()

    def carregar_todos_modelos(self):
        self.modelos.clear()
        caminho_busca = os.path.join(settings.MODELS_DIR, "*.pkl")
        arquivos_pkl = glob.glob(caminho_busca)

        if not arquivos_pkl:
            print("Nenhum modelo encontrado. Iniciando treinamento automático :)")
            sucesso = treinamento_automatico()
            if sucesso:
                arquivos_pkl = glob.glob(caminho_busca)
            else:
                print("Treinamento automático falhou. Verifique os logs para mais detalhes.")
            return

        for caminho in arquivos_pkl:
            nome_arquivo = os.path.basename(caminho)
            nome_produto = nome_arquivo.replace("modelo_", "").replace(".pkl", "")
            
            try:
                self.modelos[nome_produto] = joblib.load(caminho)
                print(f"Modelo '{nome_produto}' carregado com sucesso.")
            except Exception as e:
                print(f"Erro ao carregar modelo '{nome_produto}': {e}")

    def prever(self, dados_entrada: dict) -> dict:
        produto = dados_entrada.pop("produto", "").lower()

        if produto not in self.modelos:
            produtos_disponiveis = list(self.modelos.keys())
            raise ValueError(f"Produto '{produto}' não encontrado. Modelos disponíveis: {produtos_disponiveis}")

        # DESEMPACOTANDO O ARQUIVO SALVO
        pacote = self.modelos[produto]
        modelo_certo = pacote["modelo"]
        mae_historico = pacote["mae"]
        rmae_historico = pacote["rmae"]

        df_entrada = pd.DataFrame([dados_entrada])
        resultado = modelo_certo.predict(df_entrada)[0]

        return {
            "qtd": round(resultado, 2),
            "mae": round(mae_historico, 2),
            "rmae": round(rmae_historico, 2)
        }

modelo_preditor = ModeloPrevisao()