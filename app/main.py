from services.data_handler import buscar_caminho_arquivo, limpar_e_formatar_dados, sincronizar_feriados
from services.feature_engineering import preparar_features_semanais
from ml.trainer import treinar_modelo, avaliar_modelo

def run():
    # 1. Obter arquivo
    caminho = buscar_caminho_arquivo()
    if not caminho:
        print("Nenhum arquivo selecionado.")
        return

    # 2. Processamento Inicial
    colunas = ["qtd"]
    df = limpar_e_formatar_dados(caminho, colunas)
    df = sincronizar_feriados(df)

    # 3. Engenharia de Features
    df_preparado = preparar_features_semanais(df)

    # 4. ML (Treino e Avaliação)
    modelo, x_test, y_test = treinar_modelo(df_preparado)
    
    erros, r2, nomes = avaliar_modelo(modelo, x_test, y_test)

    print("\n--- Desempenho por Produto ---")
    for i, produto in enumerate(nomes):
        print(f"Produto: {produto}")
        print(f"  Erro Médio (MAE): {erros[i]:.2f}")
        print(f"  R² Score: {r2[i]:.2f}\n")

if __name__ == "__main__":
    run()