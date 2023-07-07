from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from .database import Base

# Modelos usados para o banco de dados

# Parent
class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("produtos.id"))

    product = relationship("Produto")

# Child
class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), unique=True, index=True)
    descricao = Column(String(100))
    preco = Column(Float)
    tipo = Column(Integer)
    
