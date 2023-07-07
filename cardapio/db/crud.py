from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from fastapi import HTTPException

try:
    from db import models, schemas
except ImportError:
    from cardapio.db import models, schemas


def get_produto(db: Session, id_produto: int):
    return db.query(models.Produto).filter(models.Produto.id == id_produto).first()

def get_produtos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Produto).offset(skip).limit(limit).all()

def create_produto(db: Session, produto: schemas.ProdutoCreate):
    db_produto = models.Produto(nome=produto.nome,
                                preco=produto.preco,
                                descricao=produto.descricao, 
                                tipo=produto.tipo)
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

def pedir_produto(db: Session, pedido: schemas.PedidoCreate):
    db_pedido = models.Pedido(nome_produto=pedido.nome_produto)
    
    pedido = db.query(models.Pedido).filter(models.Pedido.nome_produto == db_pedido.nome_produto).first()
    
    if pedido is not None:
        raise HTTPException(status_code=404, detail="Produto já pedido")
    
    try:
        db.add(db_pedido)
        db.commit()
        db.refresh(db_pedido)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return db_pedido
