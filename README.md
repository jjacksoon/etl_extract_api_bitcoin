# ETL Extract API Bitcoin

Projeto de ETL (Extract, Transform, Load) em Python para extração automática de preços do Bitcoin da API Coinbase.

## 📋 Descrição

Este projeto implementa um pipeline ETL completo que:
- **Extract**: Extrai preços do Bitcoin em tempo real da API Coinbase
- **Transform**: Transforma e padroniza os dados com timestamp
- **Load**: Armazena os dados em banco de dados (SQLite ou PostgreSQL)

O pipeline roda automaticamente coletando dados a cada 1 hora por 30 dias.

## 🛠️ Tecnologias

- **Python 3.11+**
- **requests** - Requisições HTTP à API
- **SQLAlchemy** - ORM para banco de dados
- **psycopg2** - Driver PostgreSQL (opcional)

## 📦 Instalação Local

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd etl_extract_api_bitcoin
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# ou
source .venv/bin/activate  # Linux/Mac
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 📁 Estrutura do Projeto

```
etl_extract_api_bitcoin/
│
├── src/
│   ├── pipeline.py     # Pipeline ETL principal
│   └── database.py     # Classes SQLAlchemy e DatabaseManager
│
├── requirements.txt    # Dependências do projeto
├── render.yaml         # Configuração para deploy no Render
├── Procfile            # Comando de inicialização
├── DEPLOY.md           # Guia de deploy no Render
└── README.md          # Este arquivo
```

## 🚀 Uso Local

Execute o pipeline ETL:
```bash
python src/pipeline.py
```

O pipeline irá:
- Coletar dados a cada 1 hora
- Rodar por 30 dias
- Parar automaticamente ao finalizar

## ☁️ Deploy no Render (Produção)

Para rodar 24/7 na nuvem, consulte o arquivo [DEPLOY.md](DEPLOY.md) para instruções detalhadas.

**Resumo rápido:**
1. Faça push do código para GitHub
2. Crie um Background Worker no Render
3. Configure as variáveis de ambiente
4. Deploy automático!

## ⚙️ Configuração

### Alterar Intervalo de Coleta

Edite `src/pipeline.py`:
```python
run_etl_pipeline(db, interval=3600, duration_days=30)
```

- `interval`: Segundos entre coletas (3600 = 1 hora)
- `duration_days`: Dias de coleta (30 = 1 mês)

### Banco de Dados

Por padrão usa SQLite. Para PostgreSQL:
1. Configure a variável `DATABASE_URL`
2. O código detecta automaticamente e ajusta a conexão

## 📊 Dados Coletados

Cada registro contém:
- `valor`: Preço do Bitcoin
- `criptomoeda`: BTC
- `moeda`: USD
- `timestamp`: Data/hora da coleta

## 🔧 Troubleshooting

- **Erro de conexão**: Verifique sua internet
- **Banco não conecta**: Verifique `DATABASE_URL`
- **Worker para**: Verifique logs no Render dashboard

