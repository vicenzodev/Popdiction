from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os

def treinar_modelo(df_semana):
    valores_entrada = df_semana[[
        "temp_min_semana", "temp_max_semana", "temp_media_semana",
        "umidade_media_semana", "tem_feriado_na_semana",
        "vendas_leitinho_semana_passada", "vendas_flocos_semana_passada",
        "vendas_frutao_semana_passada", "mes", "semana_do_ano"
    ]]

    valores_saida = df_semana[["qtd"]]

    entrada_train, entrada_test, saida_train, saida_test = train_test_split(
        valores_entrada, valores_saida, test_size=0.2, shuffle=False
    )

    modelo = RandomForestRegressor(n_estimators=500, random_state=42)
    modelo.fit(entrada_train, saida_train)

    # Salva o modelo na pasta 'models' conforme sua estrutura
    caminho_modelo = os.path.join('models', 'modelo_sorvetao_v1.pkl')
    joblib.dump(modelo, caminho_modelo)

    return modelo, entrada_test, saida_test

def avaliar_modelo(modelo, entrada_test, saida_test):
    previsoes = modelo.predict(entrada_test)
    erro_geral = mean_absolute_error(saida_test, previsoes)
    r2_geral = r2_score(saida_test, previsoes)

    print(f"Erro Médio Geral: {erro_geral:.2f}")
    print(f"R² Geral: {r2_geral:.2f}")
    
    erros_individuais = mean_absolute_error(saida_test, previsoes, multioutput='raw_values')
    r2_individuais = r2_score(saida_test, previsoes, multioutput='raw_values')
    
    return erros_individuais, r2_individuais, saida_test.columns