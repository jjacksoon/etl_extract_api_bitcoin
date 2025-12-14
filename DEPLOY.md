# Deploy no Render

Este guia explica como fazer deploy do pipeline ETL no Render para rodar 24/7.

## 📋 Pré-requisitos

1. Conta no [Render](https://render.com) (gratuita)
2. Repositório no GitHub com o código do projeto

## 🚀 Passo a Passo

### 1. Preparar o Repositório

Certifique-se de que seu código está no GitHub:

```bash
git add .
git commit -m "Preparar para deploy no Render"
git push origin main
```

### 2. Criar Serviço no Render

1. Acesse [Render Dashboard](https://dashboard.render.com)
2. Clique em **"New +"** → **"Background Worker"**
3. Conecte seu repositório do GitHub
4. Configure:
   - **Name**: `bitcoin-etl-pipeline`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python src/pipeline.py`
   - **Plan**: `Free` (ou escolha outro plano)

### 3. Configurar Variáveis de Ambiente

No dashboard do Render, vá em **Environment** e configure as seguintes variáveis:

#### Variáveis de Banco de Dados (Escolha uma opção)

**Opção 1: Usar DATABASE_URL (Recomendado para Render)**
- `DATABASE_URL`: URL completa do banco PostgreSQL (configurado automaticamente pelo Render se você criar um banco)

**Opção 2: Usar variáveis individuais do PostgreSQL**
- `POSTGRES_USER`: Usuário do banco de dados
- `POSTGRES_PASSWORD`: Senha do banco de dados
- `POSTGRES_HOST`: Host do banco de dados
- `POSTGRES_PORT`: Porta do banco de dados (padrão: `5432`)
- `POSTGRES_DB`: Nome do banco de dados

**Nota**: Se `DATABASE_URL` estiver definido, ele terá prioridade. Caso contrário, o código tentará construir a URL a partir das variáveis individuais. Se nenhuma estiver definida, usará SQLite como fallback.

#### Variáveis Opcionais (com valores padrão)
- `COLLECTION_INTERVAL`: Intervalo em segundos entre coletas (padrão: `3600` = 1 hora)
  - `1800` = 30 minutos
  - `900` = 15 minutos
  - `3600` = 1 hora (padrão)
  
- `API_URL`: URL da API (padrão: `https://api.coinbase.com/v2/prices/BTC-USD/spot`)
- `API_TIMEOUT`: Timeout da requisição em segundos (padrão: `10`)
- `CRYPTO_CURRENCY`: Criptomoeda a coletar (padrão: `BTC`)
- `FIAT_CURRENCY`: Moeda fiat de referência (padrão: `USD`)
- `DATA_RETENTION_DAYS`: Número de dias para manter os dados (padrão: `90`)
  - Dados mais antigos serão removidos automaticamente
  - Exemplo: `90` = mantém últimos 90 dias
- `CLEANUP_INTERVAL_HOURS`: Intervalo em horas para executar limpeza (padrão: `24`)
  - Exemplo: `24` = limpeza 1 vez por dia

**Nota**: O código funciona com SQLite por padrão, mas PostgreSQL é recomendado para produção.

### 4. Criar Banco de Dados PostgreSQL (Recomendado)

1. No Render Dashboard, clique em **"New +"** → **"PostgreSQL"**
2. Configure:
   - **Name**: `bitcoin-db`
   - **Plan**: `Free` (ou outro)
3. Copie a **Internal Database URL**
4. Adicione como variável de ambiente `DATABASE_URL` no seu Worker

### 5. Deploy Automático

O Render fará deploy automaticamente quando você fizer push no GitHub.

## 📝 Arquivos de Configuração

O projeto já inclui:
- `render.yaml`: Configuração do serviço
- `Procfile`: Comando de inicialização
- `requirements.txt`: Dependências Python

## ⚙️ Configurações Avançadas

### Alterar Intervalo de Coleta

Edite `src/pipeline.py` na linha final:
```python
run_etl_pipeline(db, interval=3600, duration_days=30)
```

- `interval`: Segundos entre coletas (3600 = 1 hora)
- `duration_days`: Dias de coleta (30 = 1 mês)

### Monitoramento

- **Logs**: Acesse os logs no dashboard do Render
- **Status**: Verifique se o worker está rodando
- **Métricas**: Visualize uso de recursos

## 🔧 Troubleshooting

### Worker para de funcionar

1. Verifique os logs no dashboard
2. Certifique-se de que o banco de dados está acessível
3. Verifique se há erros de conexão com a API

### Banco de dados não conecta

1. Verifique a variável `DATABASE_URL`
2. Para PostgreSQL, certifique-se de usar a URL interna do Render
3. Teste a conexão localmente primeiro

## 💰 Custos

**⚠️ IMPORTANTE**: O Render **não oferece Background Workers no plano gratuito**. É necessário um plano pago.

- **Starter Plan ($7/mês)**: 
  - Background Worker sempre ativo
  - 1 GB RAM
  - Ideal para produção
  - PostgreSQL gratuito disponível separadamente

- **Planos Superiores**: 
  - Mais recursos (CPU/RAM)
  - Melhor performance
  - Para cargas maiores

### Alternativas Gratuitas

Se você precisa de uma solução gratuita, considere:

1. **Railway** (railway.app)
   - Plano free com créditos mensais
   - Background workers disponíveis
   - PostgreSQL incluído

2. **Fly.io** (fly.io)
   - Plano free com limitações
   - Workers sempre ativos
   - PostgreSQL disponível

3. **PythonAnywhere** (pythonanywhere.com)
   - Plano free limitado
   - Pode rodar scripts agendados
   - SQLite incluído

4. **Replit** (replit.com)
   - Plano free disponível
   - Pode rodar scripts contínuos
   - PostgreSQL disponível

## 📊 Verificar Dados Coletados

Após o deploy, você pode:
1. Conectar ao banco PostgreSQL via cliente SQL
2. Ou criar um script para consultar os dados
3. Exportar dados do banco

## 🎯 Próximos Passos

- Configurar alertas por email
- Criar dashboard para visualizar dados
- Adicionar backup automático
- Configurar monitoramento de saúde
