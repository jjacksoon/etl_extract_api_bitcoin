# 🚀 Guia Passo a Passo - Deploy no Render

Este guia vai te ajudar a fazer deploy do pipeline ETL no Render para rodar 24/7.

## 📋 Pré-requisitos

✅ Conta no GitHub (gratuita)  
✅ Conta no Render (gratuita)  
✅ Código do projeto pronto

---

## PASSO 1: Preparar o Código no GitHub

### 1.1. Verificar se o código está no Git

Abra o terminal na pasta do projeto e execute:

```bash
git status
```

Se aparecer "not a git repository", inicialize o repositório:

```bash
git init
git add .
git commit -m "Preparar projeto para deploy no Render"
```

### 1.2. Criar Repositório no GitHub

1. Acesse [github.com](https://github.com)
2. Clique em **"New"** (ou **"+"** → **"New repository"**)
3. Configure:
   - **Repository name**: `etl-extract-api-bitcoin` (ou outro nome)
   - **Visibility**: Público ou Privado (sua escolha)
   - **NÃO marque** "Add a README file" (já temos um)
4. Clique em **"Create repository"**

### 1.3. Fazer Push do Código

No terminal, execute (substitua `SEU_USUARIO` pelo seu usuário do GitHub):

```bash
git remote add origin https://github.com/SEU_USUARIO/etl-extract-api-bitcoin.git
git branch -M main
git push -u origin main
```

**Se pedir autenticação:**
- Use um Personal Access Token (não sua senha)
- Crie em: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)

---

## PASSO 2: Criar Conta no Render

1. Acesse [render.com](https://render.com)
2. Clique em **"Get Started for Free"**
3. Faça login com GitHub (recomendado) ou crie conta com email
4. Confirme seu email se necessário

---

## PASSO 3: Criar Banco de Dados PostgreSQL

### 3.1. Criar o Banco

1. No [Render Dashboard](https://dashboard.render.com), clique em **"New +"**
2. Selecione **"PostgreSQL"**
3. Configure:
   - **Name**: `bitcoin-db`
   - **Database**: `bitcoin_db` (ou deixe padrão)
   - **User**: Deixe padrão
   - **Region**: Escolha o mais próximo (ex: Oregon)
   - **PostgreSQL Version**: Deixe a mais recente
   - **Plan**: **Free** (ou escolha outro)
4. Clique em **"Create Database"**

### 3.2. Anotar as Credenciais

1. Aguarde o banco ser criado (pode levar alguns minutos)
2. Vá em **"Connections"** ou **"Info"**
3. Anote:
   - **Internal Database URL** (vai usar depois)
   - Ou as credenciais individuais:
     - Host
     - Port
     - Database
     - User
     - Password

---

## PASSO 4: Criar Background Worker

### 4.1. Criar o Worker

1. No Render Dashboard, clique em **"New +"**
2. Selecione **"Background Worker"**
3. Conecte seu repositório GitHub:
   - Clique em **"Connect account"** se necessário
   - Autorize o Render a acessar seus repositórios
   - Selecione o repositório `etl-extract-api-bitcoin`

### 4.2. Configurar o Worker

Preencha os campos:

- **Name**: `bitcoin-etl-pipeline`
- **Region**: Mesma região do banco de dados
- **Branch**: `main` (ou `master`)
- **Root Directory**: Deixe vazio (ou `.` se pedir)
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python src/pipeline.py`
- **Plan**: **Free** (ou escolha outro)

### 4.3. Configurar Variáveis de Ambiente

Na seção **"Environment Variables"**, adicione:

#### Opção A: Usar DATABASE_URL (Mais Simples)

1. Clique em **"Add Environment Variable"**
2. **Key**: `DATABASE_URL`
3. **Value**: Cole a **Internal Database URL** que você anotou no Passo 3.2
4. Clique em **"Save Changes"**

#### Opção B: Usar Variáveis Individuais

Adicione uma por uma:

- **Key**: `POSTGRES_USER` | **Value**: (usuário do banco)
- **Key**: `POSTGRES_PASSWORD` | **Value**: (senha do banco)
- **Key**: `POSTGRES_HOST` | **Value**: (host do banco)
- **Key**: `POSTGRES_PORT` | **Value**: `5432` (ou a porta do seu banco)
- **Key**: `POSTGRES_DB` | **Value**: (nome do banco)

#### Variáveis Opcionais (Recomendado)

Adicione também:

- **Key**: `COLLECTION_INTERVAL` | **Value**: `3600` (1 hora em segundos)
- **Key**: `API_URL` | **Value**: `https://api.coinbase.com/v2/prices/BTC-USD/spot`
- **Key**: `API_TIMEOUT` | **Value**: `10`
- **Key**: `CRYPTO_CURRENCY` | **Value**: `BTC`
- **Key**: `FIAT_CURRENCY` | **Value**: `USD`

### 4.4. Criar o Worker

1. Clique em **"Create Background Worker"**
2. Aguarde o deploy (pode levar 2-5 minutos)

---

## PASSO 5: Verificar se Está Funcionando

### 5.1. Verificar Logs

1. No dashboard do Render, clique no seu worker `bitcoin-etl-pipeline`
2. Vá na aba **"Logs"**
3. Você deve ver mensagens como:
   ```
   Iniciando pipeline ETL automático...
   Coleta de dados a cada 60 minutos (3600 segundos)
   [2025-12-12 10:00:00] Coleta #1
   ```

### 5.2. Verificar Status

- **Status** deve estar **"Live"** (verde)
- Se estiver **"Build failed"**, verifique os logs de erro

### 5.3. Verificar Dados no Banco

1. Conecte ao banco PostgreSQL usando DBeaver
2. Execute:
   ```sql
   SELECT * FROM bitcoin_prices ORDER BY timestamp DESC LIMIT 10;
   ```
3. Você deve ver os dados sendo inseridos a cada hora

---

## 🔧 Troubleshooting

### Problema: Build Failed

**Solução:**
1. Verifique os logs de build
2. Certifique-se de que `requirements.txt` está correto
3. Verifique se o Python está na versão 3.11

### Problema: Worker não conecta ao banco

**Solução:**
1. Verifique se `DATABASE_URL` está correto
2. Use a **Internal Database URL** (não a externa)
3. Certifique-se de que o banco está na mesma região do worker

### Problema: Worker para de funcionar

**Solução:**
1. Verifique os logs para erros
2. No plano Free, o worker pode "dormir" após inatividade
3. Considere usar um plano pago para 24/7 garantido

### Problema: Erro de importação

**Solução:**
1. Verifique se todos os arquivos estão no GitHub
2. Certifique-se de que o caminho `src/pipeline.py` está correto

---

## ✅ Checklist Final

- [ ] Código está no GitHub
- [ ] Conta no Render criada
- [ ] Banco PostgreSQL criado
- [ ] Background Worker criado
- [ ] Variáveis de ambiente configuradas
- [ ] Worker está "Live"
- [ ] Logs mostram coletas funcionando
- [ ] Dados aparecendo no banco

---

## 🎉 Pronto!

Agora seu pipeline está rodando 24/7 no Render! Mesmo desligando seu computador, o código continuará coletando dados a cada hora.

### Próximos Passos

- Monitorar os logs periodicamente
- Verificar os dados no banco
- Considerar upgrade para plano pago (se necessário)
- Configurar alertas (opcional)

---

## 📞 Precisa de Ajuda?

Se tiver problemas, verifique:
1. Logs do Render
2. Status do worker
3. Configuração das variáveis de ambiente
4. Conectividade com o banco de dados
