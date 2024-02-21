import sqlalchemy.orm
from sqlalchemy import Identity, String, Column, Numeric, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
# import cx_Oracle

username = ''
password = ''
server = ''
port = ''
dbname = ''
oracle_client_path = ''
# oracle_client_path = 'C:\\Users\\logonrmlocal\\Downloads\\instantclient_21_10'

engine = sqlalchemy.create_engine(f"oracle+cx_oracle://{username}:{password}@{server}:{port}/{dbname}?"
                                  f"encoding=UTF-8&nencoding=UTF-8")

Session = sessionmaker(bind=engine)
session = Session()

Base = sqlalchemy.orm.declarative_base()


class TOng(Base):
    __tablename__ = 't_ong'

    id_ong = Column(Numeric(5, 0), Identity(start=1), primary_key=True)
    nome_ong = Column(String(100), nullable=False)
    email_ong = Column(String(100), nullable=False)
    senha_ong = Column(String(30), nullable=False)
    cnpj_ong = Column(String(18), nullable=True)
    endereco = relationship('TEnderecoOng', cascade='all, delete-orphan')
    pedidos = relationship('TPedidos', cascade='all, delete-orphan')

    def __repr__(self):
        return f" ----------------- \n" \
               f"ID: {self.id_ong}\n" \
               f"Nome: {self.nome_ong}\n" \
               f"Email: {self.email_ong}\n" \
               f"CNPJ: {self.cnpj_ong}\n"


class TEnderecoOng(Base):
    __tablename__ = 't_endereco_ong'

    id_endereco_ong = Column(Numeric(5, 0), Identity(start=1), primary_key=True)
    id_ong = Column(Numeric(5, 0), ForeignKey('t_ong.id_ong'), nullable=False)
    endereco_ong = Column(String(300), nullable=False)
    cidade_ong = Column(String(200), nullable=False)
    estado_ong = Column(String(200), nullable=False)

    def __repr__(self):
        return f" ----------------- \n" \
               f"ID: {self.id_endereco_ong}\n" \
               f"ID ONG: {self.id_ong}\n" \
               f"Endereço: {self.endereco_ong} - {self.cidade_ong}, {self.estado_ong}\n"


class TEstabelecimento(Base):
    __tablename__ = 't_estabelecimento'

    id_estab = Column(Numeric(5, 0), Identity(start=1), primary_key=True)
    nome_estab = Column(String(100), nullable=False)
    email_estab = Column(String(100), nullable=False)
    senha_estab = Column(String(30), nullable=False)
    cnpj_estab = Column(String(18), nullable=True)
    endereco = relationship('TEnderecoEstab', cascade='all, delete-orphan')
    pedidos = relationship('TPedidos', cascade='all, delete-orphan')

    def __repr__(self):
        return f" ----------------- \n" \
               f"ID: {self.id_estab}\n" \
               f"Nome: {self.nome_estab}\n" \
               f"Email: {self.email_estab}\n" \
               f"CNPJ: {self.cnpj_estab}\n"


class TEnderecoEstab(Base):
    __tablename__ = 't_endereco_estab'

    id_endereco_estab = Column(Numeric(5, 0), Identity(start=1), primary_key=True)
    id_estab = Column(Numeric(5, 0), ForeignKey('t_estabelecimento.id_estab'), nullable=False)
    endereco_estab = Column(String(300), nullable=False)
    cidade_estab = Column(String(200), nullable=False)
    estado_estab = Column(String(200), nullable=False)

    def __repr__(self):
        return f" ----------------- \n" \
               f"ID: {self.id_endereco_estab}\n" \
               f"ID Estab: {self.id_estab}\n" \
               f"Endereço: {self.endereco_estab} - {self.cidade_estab}, {self.estado_estab}\n"


class TPedidos(Base):
    __tablename__ = 't_pedidos'

    id_pedidos = Column(Numeric(5, 0), Identity(start=1), primary_key=True)
    id_ong = Column(Numeric(5, 0), ForeignKey('t_ong.id_ong'), nullable=True)
    id_estab = Column(Numeric(5, 0), ForeignKey('t_estabelecimento.id_estab'), nullable=True)
    item_pedidos = Column(String(200), nullable=False)
    quantidade_pedidos = Column(String(200), nullable=False)
    status_pedidos = Column(String(50), nullable=False)
    entrega = relationship('TEntrega', cascade='all, delete-orphan')

    def __repr__(self):
        return f"-----------------\n" \
               f"ID: {self.id_pedidos}\n" \
               f"ID ONG: {self.id_ong}\n" \
               f"ID ESTAB: {self.id_estab}\n" \
               f"Item: {self.item_pedidos}\n" \
               f"Quantidade: {self.quantidade_pedidos}\n" \
               f"Status: {self.status_pedidos}\n"


class TEntrega(Base):
    __tablename__ = 't_entrega'

    id_pedidos = Column(Numeric(5, 0), ForeignKey('t_pedidos.id_pedidos'), primary_key=True, nullable=False)
    data_entrega = Column(Date, nullable=False)
    endereco_entrega = Column(String(200), nullable=False)
    observacoes_entrega = Column(String(50), nullable=False)

    def __repr__(self):
        return f" ----------------- \n" \
               f"ID Pedido: {self.id_pedidos}\n" \
               f"Data: {self.data_entrega}\n" \
               f"Endereço: {self.endereco_entrega}\n" \
               f"Observações: {self.observacoes_entrega}\n"


Base.metadata.create_all(engine)
