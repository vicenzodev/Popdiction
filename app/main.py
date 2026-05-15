from services.data_handler import buscar_caminho_arquivo, limpar_e_formatar_dados, sincronizar_feriados, remover_outliers
from services.feature_engineering import preparar_features_semanais
from ml.trainer import treinar_modelo, avaliar_modelo

def run():
    caminho = buscar_caminho_arquivo()
    if not caminho:
        print("Nenhum arquivo selecionado.")
        return

    # <-- Alterado para apenas a coluna qtd
    colunas = ["qtd"]
    df = limpar_e_formatar_dados(caminho, colunas)
    df = remover_outliers(df, "qtd")
    df = sincronizar_feriados(df)

    df_preparado = preparar_features_semanais(df)

    modelo, x_test, y_test = treinar_modelo(df_preparado)
    
    # <-- Avaliação simplificada
    erro_mae, r2 = avaliar_modelo(modelo, x_test, y_test)

    print("\n--- Desempenho do Modelo (Qtd Geral) ---")
    print(f"Erro Médio (MAE): {erro_mae:.2f}")
    print(f"R² Score: {r2:.2f}")

if __name__ == "__main__":
    run()