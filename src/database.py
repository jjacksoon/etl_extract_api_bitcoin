from sqlalchemy import create_engine, Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Base para os modelos
Base = declarative_base()


class BitcoinPrice(Base):
    """Modelo para armazenar preços do Bitcoin"""
    __tablename__ = 'bitcoin_prices'
    
    id = Column(String, primary_key=True)
    valor = Column(Float, nullable=False)
    criptomoeda = Column(String(10), nullable=False)
    moeda = Column(String(10), nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.now)
    
    def __repr__(self):
        return f"<BitcoinPrice(valor={self.valor}, criptomoeda={self.criptomoeda}, moeda={self.moeda}, timestamp={self.timestamp})>"


class DatabaseManager:
    """Classe para gerenciar operações do banco de dados"""
    
    def __init__(self, database_url='sqlite:///bitcoin.db'):
        """
        Inicializa o gerenciador do banco de dados
        
        Args:
            database_url: URL de conexão do banco (padrão: SQLite)
        """
        self.engine = create_engine(database_url, echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)
    
    def create_tables(self):
        """Cria todas as tabelas definidas nos modelos"""
        Base.metadata.create_all(self.engine)
        print("Tabelas criadas com sucesso!")
    
    def insert_price(self, valor, criptomoeda, moeda, timestamp=None):
        """
        Insere um novo registro de preço
        
        Args:
            valor: Valor do Bitcoin
            criptomoeda: Nome da criptomoeda (ex: BTC)
            moeda: Moeda de referência (ex: USD)
            timestamp: Data/hora (padrão: agora)
        
        Returns:
            BitcoinPrice: Objeto criado
        """
        session = self.SessionLocal()
        try:
            if timestamp is None:
                timestamp = datetime.now()
            elif isinstance(timestamp, str):
                timestamp = datetime.fromisoformat(timestamp)
            
            # Gera ID único baseado no timestamp
            price_id = f"{criptomoeda}_{moeda}_{timestamp.isoformat()}"
            
            new_price = BitcoinPrice(
                id=price_id,
                valor=float(valor),
                criptomoeda=criptomoeda,
                moeda=moeda,
                timestamp=timestamp
            )
            
            session.add(new_price)
            session.commit()
            print(f"Dados inseridos com sucesso! ID: {price_id}")
            return new_price
        except Exception as e:
            session.rollback()
            print(f"Erro ao inserir dados: {e}")
            raise
        finally:
            session.close()
    
    def insert_from_dict(self, dados_transformados):
        """
        Insere dados a partir de um dicionário
        
        Args:
            dados_transformados: Dicionário com chaves: valor, criptomoeda, moeda, timestamp
        """
        return self.insert_price(
            valor=dados_transformados['valor'],
            criptomoeda=dados_transformados['criptomoeda'],
            moeda=dados_transformados['moeda'],
            timestamp=dados_transformados.get('timestamp')
        )
    
    def get_all_prices(self):
        """Retorna todos os preços armazenados"""
        session = self.SessionLocal()
        try:
            prices = session.query(BitcoinPrice).order_by(BitcoinPrice.timestamp.desc()).all()
            return prices
        finally:
            session.close()
    
    def get_latest_price(self):
        """Retorna o preço mais recente"""
        session = self.SessionLocal()
        try:
            latest = session.query(BitcoinPrice).order_by(BitcoinPrice.timestamp.desc()).first()
            return latest
        finally:
            session.close()
    
    def get_prices_by_date_range(self, start_date, end_date):
        """
        Retorna preços em um intervalo de datas
        
        Args:
            start_date: Data inicial (datetime ou string ISO)
            end_date: Data final (datetime ou string ISO)
        """
        session = self.SessionLocal()
        try:
            if isinstance(start_date, str):
                start_date = datetime.fromisoformat(start_date)
            if isinstance(end_date, str):
                end_date = datetime.fromisoformat(end_date)
            
            prices = session.query(BitcoinPrice).filter(
                BitcoinPrice.timestamp >= start_date,
                BitcoinPrice.timestamp <= end_date
            ).order_by(BitcoinPrice.timestamp.desc()).all()
            
            return prices
        finally:
            session.close()
    
    def close(self):
        """Fecha a conexão com o banco"""
        self.engine.dispose()


# Exemplo de uso
if __name__ == "__main__":
    # Criar instância do gerenciador
    db = DatabaseManager()
    
    # Criar tabelas
    db.create_tables()
    
    # Exemplo de inserção
    dados_exemplo = {
        'valor': '92316.00',
        'criptomoeda': 'BTC',
        'moeda': 'USD',
        'timestamp': datetime.now().isoformat()
    }
    
    db.insert_from_dict(dados_exemplo)
    
    # Buscar último preço
    latest = db.get_latest_price()
    print(f"\nÚltimo preço: {latest}")
    
    # Buscar todos
    all_prices = db.get_all_prices()
    print(f"\nTotal de registros: {len(all_prices)}")
    
    db.close()
