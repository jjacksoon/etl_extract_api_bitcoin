import requests as req
from datetime import datetime
import time
import os
from database import DatabaseManager


def extract(api_url=None, timeout=None):
    """
    Extrai dados da API da Coinbase
    
    Args:
        api_url: URL da API (padrão: obtido de variável de ambiente ou padrão)
        timeout: Timeout da requisição em segundos (padrão: obtido de variável de ambiente ou 10)
    
    Returns:
        dict: Dados JSON da API
    """
    if api_url is None:
        api_url = os.getenv('API_URL', 'https://api.coinbase.com/v2/prices/BTC-USD/spot')
    if timeout is None:
        timeout = int(os.getenv('API_TIMEOUT', '10'))
    
    try:
        response = req.get(api_url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except req.exceptions.RequestException as e:
        print(f"Erro ao extrair dados da API: {e}")
        raise


def transform(data, criptomoeda=None, moeda_fiat=None):
    """
    Transforma os dados da API em formato padronizado
    
    Args:
        data: Dados brutos da API
        criptomoeda: Nome da criptomoeda (padrão: obtido de variável de ambiente ou 'BTC')
        moeda_fiat: Moeda fiat (padrão: obtido de variável de ambiente ou 'USD')
        
    Returns:
        dict: Dados transformados com timestamp
    """
    try:
        valor = data['data']['amount']
        moeda = data['data']['currency']
        
        # Usar variáveis de ambiente ou padrões
        if criptomoeda is None:
            criptomoeda = os.getenv('CRYPTO_CURRENCY', 'BTC')
        if moeda_fiat is None:
            moeda_fiat = os.getenv('FIAT_CURRENCY', 'USD')
        
        timestamp = datetime.now().isoformat()
        
        dados_transformados = {
            'valor': valor,
            'criptomoeda': criptomoeda,
            'moeda': moeda,
            'timestamp': timestamp
        }
        return dados_transformados
    except KeyError as e:
        print(f"Erro ao transformar dados: campo não encontrado - {e}")
        raise


def load(dados_transformados, db_manager):
    """
    Carrega dados transformados no banco de dados
    
    Args:
        dados_transformados: Dicionário com dados transformados
        db_manager: Instância do DatabaseManager
    """
    try:
        db_manager.insert_from_dict(dados_transformados)
    except Exception as e:
        print(f"Erro ao carregar dados no banco: {e}")
        raise


def run_etl_pipeline(db_manager, interval=3600):
    """
    Executa o pipeline ETL completo de forma contínua
    
    Args:
        db_manager: Instância do DatabaseManager
        interval: Intervalo em segundos entre coletas (padrão: 3600 = 1 hora)
    """
    start_time = datetime.now()
    
    print("=" * 60)
    print("Iniciando pipeline ETL automático...")
    print(f"Coleta de dados a cada {interval // 60} minutos ({interval} segundos)")
    print(f"Data de início: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("Pipeline rodando continuamente...")
    print("=" * 60)
    print()
    
    coleta_count = 0
    
    while True:
        try:
            current_time = datetime.now()
            
            # Extract
            print(f"[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] Coleta #{coleta_count + 1}")
            print("Extraindo dados...")
            
            dados = extract()
            
            # Transform
            dados_transformados = transform(dados)
            print(f"Dados transformados: {dados_transformados['criptomoeda']} = {dados_transformados['valor']} {dados_transformados['moeda']}")
            
            # Load
            load(dados_transformados, db_manager)
            
            coleta_count += 1
            
            print(f"Próxima coleta em {interval // 60} minutos ({interval} segundos)...")
            print()
            time.sleep(interval)
                
        except Exception as e:
            print(f"Erro no pipeline: {e}")
            print(f"Aguardando {interval // 60} minutos antes de tentar novamente...\n")
            time.sleep(interval)


def get_database_url():
    """
    Constrói a URL do banco de dados a partir de variáveis de ambiente individuais
    ou usa DATABASE_URL se disponível
    
    Returns:
        str: URL de conexão do banco de dados
    """
    # Se DATABASE_URL estiver definido, usar ele (prioridade)
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        # Se for PostgreSQL do Render, ajustar a URL
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        return database_url
    
    # Caso contrário, construir a URL a partir de variáveis individuais
    postgres_user = os.getenv('POSTGRES_USER')
    postgres_password = os.getenv('POSTGRES_PASSWORD')
    postgres_host = os.getenv('POSTGRES_HOST')
    postgres_port = os.getenv('POSTGRES_PORT', '5432')
    postgres_db = os.getenv('POSTGRES_DB')
    
    # Se todas as variáveis do PostgreSQL estiverem definidas, construir URL
    if all([postgres_user, postgres_password, postgres_host, postgres_db]):
        database_url = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
        return database_url
    
    # Fallback para SQLite
    return 'sqlite:///bitcoin.db'


if __name__ == "__main__":
    # Carregar variáveis de ambiente
    from dotenv import load_dotenv
    load_dotenv()
    
    # Obter URL do banco de dados
    database_url = get_database_url()
    
    # Obter intervalo de coleta de variável de ambiente (em segundos)
    # Padrão: 3600 segundos (1 hora)
    collection_interval = int(os.getenv('COLLECTION_INTERVAL', '3600'))
    
    # Inicializar gerenciador do banco de dados
    db = DatabaseManager(database_url=database_url)
    
    # Criar tabelas se não existirem
    db.create_tables()
    
    # Executar pipeline ETL
    # Intervalo configurável via variável de ambiente COLLECTION_INTERVAL
    # Pipeline roda continuamente no servidor
    run_etl_pipeline(db, interval=collection_interval)