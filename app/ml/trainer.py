from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from services.data_handler import carregar_dados, remover_outliers, sincronizar_feriados
from services.feature_engineering import preparar_features_semanais
import joblib
import os


def treinar_modelo(df_semana, nome_produto):
    valores_entrada = df_semana[[
        "temp_min_semana", "temp_max_semana", "temp_media_semana",
        "umidade_media_semana", "tem_feriado_na_semana",
        "vendas_semana_passada", "mes", "semana_do_ano" # <-- Apenas uma variável de venda passada
    ]]

    valores_saida = df_semana[["qtd"]] # <-- Única saída

    entrada_train, entrada_test, saida_train, saida_test = train_test_split(
        valores_entrada, valores_saida, test_size=0.2, shuffle=False
    )

    modelo = RandomForestRegressor(n_estimators=500, random_state=42)
    
    # O scikit-learn prefere que saídas únicas sejam um array 1D, então usamos o .values.ravel()
    modelo.fit(entrada_train, saida_train.values.ravel())

    nome_arquivo = f"modelo_{nome_produto}.pkl"
    os.makedirs('models', exist_ok=True)
    caminho_modelo = os.path.join('models', nome_arquivo)

    joblib.dump(modelo, caminho_modelo)

    return modelo, entrada_test, saida_test

def avaliar_modelo(modelo, entrada_test, saida_test):
    previsoes = modelo.predict(entrada_test)
    erro_geral = mean_absolute_error(saida_test, previsoes)
    r2_geral = r2_score(saida_test, previsoes)

    # Como agora é só um produto, o erro geral já é o erro do produto
    return erro_geral, r2_geral

def treinamento_automatico():
    print("Iniciando treinamento automático...")

    df_completo = carregar_dados()

    if df_completo.empty:
        print("Aviso: O banco de dados está vazio. Faça a carga inicial")
        return False

    produtos_existentes = df_completo['produto'].unique()

    for produto in produtos_existentes:
        print(f"\n--- Treinando modelo para: {produto.upper()} ---")
        df_produto = df_completo[df_completo['produto'] == produto].copy()
        df_produto = remover_outliers(df_produto, "qtd")
        df_produto = sincronizar_feriados(df_produto)
        df_preparado = preparar_features_semanais(df_produto)

        if df_preparado.empty:
            print(f"Aviso: Não há dados suficientes para treinar o modelo de {produto}.")
            continue
        
        modelo, x_test, y_test = treinar_modelo(df_preparado,nome_produto=produto)
        erro_mae, r2 = avaliar_modelo(modelo, x_test, y_test)
        print(f"[{produto.upper()}] MAE: {erro_mae:.2f} | R2: {r2:.2f}")

    return True