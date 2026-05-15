from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os

def treinar_modelo(df_semana):
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

    caminho_modelo = os.path.join('models', 'modelo_sorvetao_v1.pkl')
    joblib.dump(modelo, caminho_modelo)

    return modelo, entrada_test, saida_test

def avaliar_modelo(modelo, entrada_test, saida_test):
    previsoes = modelo.predict(entrada_test)
    erro_geral = mean_absolute_error(saida_test, previsoes)
    r2_geral = r2_score(saida_test, previsoes)

    # Como agora é só um produto, o erro geral já é o erro do produto
    return erro_geral, r2_geral