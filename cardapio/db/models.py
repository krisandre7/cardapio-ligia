from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

try:
    from db.database import Base
except ImportError:
    from cardapio.db.database import Base

# Modelos usados para o banco de dados

# Parent
class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    id_produto = Column(Integer, ForeignKey("produtos.id"))

    produto = relationship("Produto")

# Child
class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), unique=True)
    descricao = Column(String(100))
    preco = Column(Float)
    tipo = Column(Integer)
    
