from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, insert, MetaData, Table, Float
from sqlalchemy.ext.declarative import declarative_base
import pymssql

Base = declarative_base();
Base_Testes = declarative_base();

#Tabela de Letras
class Letras(Base):
    __tablename__ = "Letras"
    Cod_Letra = Column(Integer, primary_key=True)
    Artista = Column(String)
    Nome = Column(Integer)
    Letra = Column(String)  
    
#Tabela das Classificações
class Letra_Classificacoes(Base):
    __tablename__ = "Letra_Classificacoes"
    Cod_Letra_Classificacoes = Column(Integer, primary_key=True)
    Cod_Letra = Column(Integer)
    Valencia = Column(Integer)
    Assunto = Column(Integer)
    Identificador = Column(Integer)

#Tabela de resultados ML
class Dados_Testes(Base_Testes):
    __tablename__ = "Dados_Testes"
    id = Column(Integer, primary_key=True,autoincrement=True)
    Teste = Column(String)
    Target = Column(String)
    method = Column(String)
    hyperP = Column(Integer)
    Binario = Column(Integer)
    PoS = Column(Integer)
    RemoveStopWords = Column(Integer)
    features = Column(Integer)
    components = Column(Integer)
    f1score = Column(Float)
    f1score_g5 = Column(Float)
    f1score_g4 = Column(Float)
    f1score_g3 = Column(Float)
    f1scores = Column(String)
    score = Column(Float)
    score_g5 = Column(Float)
    score_g4 = Column(Float)
    score_g3 = Column(Float)
    cfn_matrix = Column(String)
    
def CreateBaseTestes():
    liteengine = create_engine('sqlite:///Testes.db')
    Base_Testes.metadata.create_all(liteengine)
    conn_sqllite = liteengine.connect()
    
#Insere um resultado
def InserirTeste(Teste,
                Target,
                method,
                hyperP,
                Binario,
                PoS,
                RemoveStopWords,
                features,
                components,
                f1score,
                f1score_g5,
                f1score_g4,
                f1score_g3,
                f1scores,
                score,
                score_g5,
                score_g4,
                score_g3,
                cfn_matrix):
    liteengine = create_engine('sqlite:///Testes.db')
    conn_sqllite = liteengine.connect()
    ins = Dados_Testes.__table__.insert().values(Teste=Teste,
                                                Target=Target,
                                                method=method,
                                                hyperP=hyperP,
                                                Binario=Binario,
                                                PoS=PoS,
                                                RemoveStopWords=RemoveStopWords,
                                                features=features,
                                                components=components,
                                                f1score=f1score,
                                                f1score_g5=f1score_g5,
                                                f1score_g4=f1score_g4,
                                                f1score_g3=f1score_g3,
                                                f1scores=f1scores,
                                                score=score,
                                                score_g5=score_g5,
                                                score_g4=score_g4,
                                                score_g3=score_g3,
                                                cfn_matrix=cfn_matrix)
    conn_sqllite.execute(ins)

def SelectTeste(SQL):
    conn = create_engine('sqlite:///Testes.db').connect()
    resultados = conn.execute(SQL)
    return resultados.fetchall()
    
def SQLiteConn():
    liteengine = create_engine('sqlite:///Base.db');
    return liteengine.connect();

#Classificações das letras
def GetLetraClassificacoes():
    conn = SQLiteConn();
    return conn.execute('select l.Letra,lc.* from Letra_Classificacoes lc, Letras l where l.Cod_Letra = lc.Cod_Letra').fetchall();

#Classificações das letras, retornando o total de classificações, a primeira (classificação) mais comum e a segunda mais comum
def GetLetraClassificacoes_MostCommon():
    conn = SQLiteConn();
    return conn.execute("""select l.Cod_Letra,l.Letra, (select count(*)     from Letra_Classificacoes lcV where lcV.Cod_Letra = l.Cod_Letra) Total,
(select lcV.Valencia from Letra_Classificacoes lcV where lcV.Cod_Letra = l.Cod_Letra group by lcV.Valencia order by count(*) desc LIMIT 1) Valencia,
(select count(*)     from Letra_Classificacoes lcV where lcV.Cod_Letra = l.Cod_Letra group by lcV.Valencia order by count(*) desc LIMIT 1) Valencia_QTD_MC,
(select count(*)     from Letra_Classificacoes lcV where lcV.Cod_Letra = l.Cod_Letra group by lcV.Valencia order by count(*) desc LIMIT 1 OFFSET 1) Valencia_QTD_MC_2,
(select lcA.Assunto from Letra_Classificacoes lcA where lcA.Cod_Letra = l.Cod_Letra group by lcA.Assunto order by count(*) desc LIMIT 1) Assunto,
(select count(*)    from Letra_Classificacoes lcA where lcA.Cod_Letra = l.Cod_Letra group by lcA.Assunto order by count(*) desc LIMIT 1) Assunto_QTD_MC,
(select count(*)    from Letra_Classificacoes lcA where lcA.Cod_Letra = l.Cod_Letra group by lcA.Assunto order by count(*) desc LIMIT 1 OFFSET 1) Assunto_QTD_MC_2
from Letras l 
group by l.Cod_Letra""").fetchall();
        