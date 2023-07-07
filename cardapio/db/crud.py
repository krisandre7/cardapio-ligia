from sqlalchemy.orm import Session

from db import models, schemas


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
    print("no le epic pizza time")
    db.refresh(db_produto)
    return db_produto

def get_pedido(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Pedido).offset(skip).limit(limit).all()

def pedir_produto(db: Session, produto: schemas.PedidoCreate):
    db_produto = models.Pedido(produto_id=produto.nome_produto)
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto
