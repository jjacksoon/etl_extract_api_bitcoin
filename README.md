# ETL Extract API Bitcoin

Projeto de ETL (Extract, Transform, Load) em Python para extração de dados de API usando a biblioteca `requests`.

## 📋 Descrição

Este projeto implementa um pipeline ETL básico para extrair dados de uma API, realizar transformações e carregar os dados processados.

## 🛠️ Tecnologias

- Python 3.8+
- requests - Para requisições HTTP à API

## 📦 Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd etl_extract_api_bitcoin
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/Mac
```

3. Instale as dependências:
```bash
pip install requests
```

Ou usando requirements.txt:
```bash
pip install -r requirements.txt
```

## 📁 Estrutura do Projeto

```
etl_extract_api_bitcoin/
│
├── src/
│   ├── extract.py      # Extração de dados da API
│   ├── transform.py    # Transformação dos dados
│   ├── load.py         # Carregamento dos dados
│   └── main.py         # Script principal
│
├── data/               # Dados extraídos e processados
├── requirements.txt    # Dependências do projeto
└── README.md          # Este arquivo
```

## 🚀 Uso

Execute o pipeline ETL:
```bash
python src/main.py
```

## ⚙️ Configuração

Configure a URL da API e outras variáveis conforme necessário no código ou através de variáveis de ambiente.

