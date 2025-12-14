# ETL Extract API Bitcoin

Projeto de ETL (Extract, Transform, Load) em Python para extração automática de preços do Bitcoin da API Coinbase.

## 📋 Descrição

Este projeto implementa um pipeline ETL completo que:
- **Extract**: Extrai preços do Bitcoin em tempo real da API Coinbase
- **Transform**: Transforma e padroniza os dados com timestamp
- **Load**: Armazena os dados em banco de dados (SQLite ou PostgreSQL)
- **Limpeza Automática**: Remove dados antigos mantendo apenas os últimos 90 dias

O pipeline roda automaticamente coletando dados a cada 1 hora de forma contínua, com limpeza automática para manter apenas os dados recentes.

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
├── runtime.txt         # Versão do Python
├── DEPLOY.md           # Guia de deploy no Render
├── GUIA_DEPLOY_RENDER.md  # Guia passo a passo detalhado
└── README.md          # Este arquivo
```

## 🚀 Uso Local

Execute o pipeline ETL:
```bash
python src/pipeline.py
```

O pipeline irá:
- Coletar dados a cada 1 hora de forma contínua
- Executar limpeza automática mantendo apenas os últimos 90 dias
- Rodar indefinidamente até ser interrompido

## ☁️ Deploy no Render (Produção)

Para rodar 24/7 na nuvem, consulte o arquivo [DEPLOY.md](DEPLOY.md) para instruções detalhadas.

**Resumo rápido:**
1. Faça push do código para GitHub
2. Crie um Background Worker no Render
3. Configure as variáveis de ambiente
4. Deploy automático!

## ⚙️ Configuração

### Variáveis de Ambiente

O projeto suporta configuração via variáveis de ambiente. Crie um arquivo `.env` na raiz do projeto:

```env
# Banco de Dados (escolha uma opção)
DATABASE_URL=postgresql://user:pass@host:5432/dbname
# OU use variáveis individuais:
POSTGRES_USER=usuario
POSTGRES_PASSWORD=senha
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=bitcoin_db

# Configuração do Pipeline
COLLECTION_INTERVAL=3600          # Intervalo entre coletas em segundos (padrão: 3600 = 1 hora)
DATA_RETENTION_DAYS=90            # Dias para manter os dados (padrão: 90)
CLEANUP_INTERVAL_HOURS=24         # Intervalo de limpeza em horas (padrão: 24 = 1 vez por dia)

# Configuração da API
API_URL=https://api.coinbase.com/v2/prices/BTC-USD/spot
API_TIMEOUT=10
CRYPTO_CURRENCY=BTC
FIAT_CURRENCY=USD
```

### Banco de Dados

**Opção 1: SQLite (padrão)**
- Não requer configuração
- Ideal para desenvolvimento local

**Opção 2: PostgreSQL**
- Configure `DATABASE_URL` ou variáveis individuais (`POSTGRES_*`)
- Recomendado para produção
- O código detecta automaticamente e ajusta a conexão

### Intervalo de Coleta

Configure via variável de ambiente `COLLECTION_INTERVAL`:
- `3600` = 1 hora (padrão)
- `1800` = 30 minutos
- `900` = 15 minutos

### Limpeza Automática

Configure via variáveis de ambiente:
- `DATA_RETENTION_DAYS`: Dias para manter os dados (padrão: `90`)
- `CLEANUP_INTERVAL_HOURS`: Frequência da limpeza em horas (padrão: `24` = 1 vez por dia)

## 📊 Dados Coletados

Cada registro contém:
- `id`: ID único do registro
- `valor`: Preço do Bitcoin (Float)
- `criptomoeda`: BTC (String)
- `moeda`: USD (String)
- `timestamp`: Data/hora da coleta (DateTime)

### Limpeza Automática

O pipeline executa limpeza automática periodicamente:
- Remove dados mais antigos que o período de retenção configurado
- Mantém apenas os últimos N dias (padrão: 90 dias)
- Executa a cada 24 horas (configurável)
- Logs informativos sobre registros removidos

## 🔧 Troubleshooting

### Erros Comuns

- **Erro de conexão com API**: Verifique sua internet e a URL da API
- **Banco não conecta**: 
  - Verifique `DATABASE_URL` ou variáveis `POSTGRES_*`
  - Certifique-se de que o banco está acessível
- **Worker para no Render**: 
  - Verifique logs no dashboard do Render
  - No plano Free, o worker pode "dormir" após inatividade
- **Erro de importação**: 
  - Verifique se todas as dependências estão instaladas
  - Execute `pip install -r requirements.txt`

### Verificar Dados

Conecte ao banco e execute:
```sql
-- Ver últimos registros
SELECT * FROM bitcoin_prices ORDER BY timestamp DESC LIMIT 10;

-- Contar total de registros
SELECT COUNT(*) FROM bitcoin_prices;

-- Ver dados por período
SELECT * FROM bitcoin_prices 
WHERE timestamp >= NOW() - INTERVAL '7 days'
ORDER BY timestamp DESC;
```

## 📚 Documentação Adicional

- [DEPLOY.md](DEPLOY.md) - Guia de deploy no Render
- [GUIA_DEPLOY_RENDER.md](GUIA_DEPLOY_RENDER.md) - Guia passo a passo detalhado

## 🎯 Funcionalidades

✅ Coleta automática contínua  
✅ Limpeza automática de dados antigos  
✅ Suporte a SQLite e PostgreSQL  
✅ Configuração via variáveis de ambiente  
✅ Deploy fácil no Render  
✅ Logs detalhados  
✅ Tratamento de erros robusto  

## 📝 Licença

Este projeto é de código aberto e está disponível para uso educacional e comercial.

