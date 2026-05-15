import pandas as pd

def preparar_features_semanais(df):
    df.set_index('data', inplace=True)
    df = pd.get_dummies(df, columns=['loja', 'cidade'])

    df_semana = df.resample('W').agg({
        'temp_media': ['min', 'max', 'mean'],
        'umidade_media': 'mean',
        'e_feriado': 'max',
        'qtd_leitinho_5l': 'sum',
        'qtd_flocos_1l': 'sum',
        'qtd_frutao_uva': 'sum'
    }).reset_index()

    df_semana.columns = [
        'data_fim_semana', 'temp_min_semana', 'temp_max_semana', 'temp_media_semana', 
        'umidade_media_semana', 'tem_feriado_na_semana', 'qtd_leitinho_5l', 
        'qtd_flocos_1l', 'qtd_frutao_uva'
    ]

    df_semana['mes'] = df_semana['data_fim_semana'].dt.month
    df_semana['semana_do_ano'] = df_semana['data_fim_semana'].dt.isocalendar().week.astype(int)
    
    dia_do_mes_fim_semana = df_semana['data_fim_semana'].dt.day
    df_semana['semana_de_pagamento'] = dia_do_mes_fim_semana.between(5, 10).astype(int)

    # Lags (Vendas da semana anterior)
    df_semana['temp_media_semana_passada'] = df_semana['temp_media_semana'].shift(1)
    df_semana['vendas_leitinho_semana_passada'] = df_semana['qtd_leitinho_5l'].shift(1)
    df_semana['vendas_flocos_semana_passada'] = df_semana['qtd_flocos_1l'].shift(1)
    df_semana['vendas_frutao_semana_passada'] = df_semana['qtd_frutao_uva'].shift(1)

    return df_semana.dropna()