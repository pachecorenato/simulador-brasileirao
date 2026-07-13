from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base

# 1. O "Motor": Conecta ao banco (ou cria um arquivo novo chamado brasileirao.db)
motor = create_engine('sqlite:///brasileirao.db', echo=True)

# 2. A "Base": O SQLAlchemy precisa dessa classe base para entender nossos moldes
Base = declarative_base()

# 3. A Tabela: Criamos a estrutura usando Orientação a Objetos
class TimeHistorico(Base):
    """Modelo ORM (SQLAlchemy) que representa o histórico consolidado de um time.

    Mapeia a tabela 'historico_serie_a' no banco SQLite 'brasileirao.db',
    armazenando os totais acumulados de participações, pontos, vitórias,
    empates e derrotas de cada time ao longo das temporadas coletadas.

    Attributes:
        id (int): Identificador único do registro (chave primária,
            gerado automaticamente pelo banco de dados).
        nome (str): Nome do time. É único (unique=True), impedindo que
            o mesmo time seja cadastrado mais de uma vez.
        participacoes (int): Número de temporadas em que o time
            participou da Série A dentro do período coletado.
        pontos (int): Soma total de pontos conquistados pelo time em
            todas as temporadas consideradas.
        vitorias (int): Soma total de vitórias do time.
        empates (int): Soma total de empates do time.
        derrotas (int): Soma total de derrotas do time.
    """
    __tablename__ = 'historico_serie_a'
    
    # Definindo as colunas da tabela
    id = Column(Integer, primary_key=True) # ID único de cada registro
    nome = Column(String, unique=True)     # unique=True impede que o mesmo time seja salvo duas vezes
    participacoes = Column(Integer)
    pontos = Column(Integer)
    vitorias = Column(Integer)
    empates = Column(Integer)
    derrotas = Column(Integer)

# 4. O Comando de Criação: Pega os moldes e constrói a tabela fisicamente no arquivo
Base.metadata.create_all(motor)

print("\nBanco de Dados 'brasileirao.db' e tabela criados com sucesso!")
