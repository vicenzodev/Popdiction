from app.services.data_handler import buscar_caminho_arquivo, importar_csv 

def rodar_carga():
    print("aguardando a seleção do arquivo...")

    caminho = buscar_caminho_arquivo()

    if not caminho:
        print("Nenhum arquivo selecionado.")
        return
    
    importar_csv(caminho)

if __name__ == "__main__":
    rodar_carga()