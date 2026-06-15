# API Previsão de Sorvetes

Este repositório contém uma API REST desenvolvida com FastAPI para previsão de demanda de sorvetes por produto.

## Visão geral

- A aplicação principal está em `app/main.py`
- Os endpoints estão em `app/api/endpoints.py`
- A inferência de previsão usa `app/ml/inference.py`
- O treinamento automático e a geração de modelos estão em `app/ml/trainer.py`
- O preenchimento de dados de contexto (clima, feriado, vendas passadas) está em `app/services/context.py`
- Os dados brutos e o banco SQLite estão em `data/` e `dados_processados.db`

## Endpoints disponíveis

### Health check

- Método: `GET`
- URL: `/`
- Resposta:
  - `status`: `online`
  - `mensagem`: texto informativo

### Previsão de demanda

- Método: `POST`
- URL: `/api/v1/prever`
- Request JSON:
  ```json
  {
    "produto": "tabela_flocos_1l",
    "data": "2026-06-15"
  }
  ```
- Campos esperados:
  - `produto`: string com o nome do produto. Deve corresponder a um modelo disponível, por exemplo:
    - `tabela_flocos_1l`
    - `tabela_frutao_uva`
    - `tabela_leitinho_5l`
  - `data`: string de data no formato compatível com `pandas.to_datetime`, como `YYYY-MM-DD`

- Resposta JSON:
  ```json
  {
    "qtd": 123.45,
    "mae": 1.23,
    "rmae": 5.67
  }
  ```

- O endpoint constrói internamente os dados de contexto necessários para o modelo:
  - `temp_min_semana`
  - `temp_max_semana`
  - `temp_media_semana`
  - `umidade_media_semana`
  - `tem_feriado_na_semana`
  - `vendas_semana_passada`
  - `mes`
  - `semana_do_ano`

- Observações importantes:
  - A API usa `brasilapi.com.br` para feriados e `open-meteo.com` para clima.
  - Se alguma chamada externa falhar, valores padrões são usados.
  - O parâmetro `produto` é convertido para minúsculas ao buscar o modelo.

### Treinamento automático

- Método: `POST`
- URL: `/api/v1/treinar`
- Request body: vazio
- Resposta:
  ```json
  {
    "status": 200,
    "mensagem": "O modelo começou a ser treinado"
  }
  ```
- Esse endpoint dispara um trabalho em background que:
  1. Carrega os dados do banco SQLite (`dados_processados.db`)
  2. Treina um modelo para cada produto presente no histórico
  3. Salva os modelos em `app/models/modelo_<produto>.pkl`
  4. Atualiza a memória de modelos em `app/ml/inference.py`

### Inserir dados de histórico via API

O endpoint `/api/v1/historico/importar` permite adicionar novos registros diretamente ao banco de dados SQLite usado pela API.

- Método: `POST`
- URL: `/api/v1/historico/importar`
- Request JSON: array de objetos

```json
[
  {
    "data": "2026-06-08",
    "loja": "loja_a",
    "cidade": "Cidade X",
    "produto": "tabela_flocos_1l",
    "qtd": 3500.0
  },
  {
    "data": "2026-06-09",
    "loja": "loja_a",
    "cidade": "Cidade X",
    "produto": "tabela_flocos_1l",
    "qtd": 4200.0
  }
]
```

- Resposta JSON:

```json
{
  "status": 200,
  "mensagem": "Dados do histórico importados com sucesso",
  "registros_inseridos": 2,
  "duplicatas_removidas": 0
}
```

- A rota grava os registros na tabela `historico_vendas` do banco `dados_processados.db`.
- Campos obrigatórios:
  - `data`
  - `loja`
  - `cidade`
  - `produto`
  - `qtd`
- A API remove duplicatas com a mesma combinação `data` + `loja` + `produto`, mantendo o registro mais recente.

#### Exemplo curl para inserir dados

```powershell
curl -X POST http://127.0.0.1:8000/api/v1/historico/importar \
  -H "Content-Type: application/json" \
  -d "[{\"data\": \"2026-06-08\", \"loja\": \"loja_a\", \"cidade\": \"Cidade X\", \"produto\": \"tabela_flocos_1l\", \"qtd\": 3500.0}]"
```

## Como executar localmente

1. Abra o terminal na pasta do projeto:
   ```powershell
   cd c:\Users\heito\Documents\Fatec\5Sem\TG\algoritmo\api
   ```

2. Instale os pacotes necessários. O arquivo `requirements.txt` está vazio neste repositório, mas as dependências usadas são:
   ```powershell
   python -m pip install fastapi uvicorn pandas scikit-learn joblib requests pydantic
   ```

3. Inicie o servidor:
   ```powershell
   python app\main.py
   ```

4. Acesse a documentação automática do FastAPI no navegador:
   - `http://127.0.0.1:8000/docs`
   - `http://127.0.0.1:8000/redoc`

## Preparação de dados

O projeto também contém um script de carga inicial em `carga_inicial.py`.

- Ele abre um diálogo para selecionar arquivos CSV.
- Os arquivos carregados são importados para a tabela `historico_vendas` dentro do banco SQLite (`dados_processados.db`).
- O nome do produto é extraído do nome do arquivo CSV.

### Estrutura esperada dos CSVs

O CSV deve conter, pelo menos, as colunas:
- `data`
- `qtd`
- `loja`
- `cidade`

Os dados são convertidos internamente para datas e normalizados.

## Observações finais

- Se não houver modelos salvos em `app/models/`, o carregamento do preditor tenta treinar automaticamente.
- Os nomes de produto no endpoint de previsão devem ser os mesmos que aparecem nos arquivos de modelo salvos.
- Caso seja necessário, preencha `requirements.txt` com as dependências acima para facilitar a instalação.
