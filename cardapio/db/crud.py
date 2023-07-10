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

def delete_produtos(db: Session):
    db.query(models.Produto).delete()
    db.commit()
    return {"message": "Produtos deletados com sucesso"}

def clear_db(db: Session):
    db.query(models.Pedido).delete()
    db.query(models.Produto).delete()
    db.commit()
    return {"message": "Banco de dados limpo"}

def create_produto(db: Session, produto: schemas.ProdutoCreate):
    #verifica se o produto é vazio
    if produto.nome == "" or produto.nome == " ":
        raise HTTPException(status_code=400, detail="Nome invalido")
    #verifica se a descrição é vazio
    if not produto.descricao:
        raise HTTPException(status_code=400, detail="A descrição não pode ser vazio")
    #verifica se o preço é diferente de zero ou negativo
    if produto.preco <= 0:
        raise HTTPException(status_code=400, detail="O valor precisa ser maior que zero")
    #verifica o tipo do produto
    if produto.tipo != 0 and produto.tipo != 1:
        raise HTTPException(status_code=400, detail="Tipo do produto desconhecido")
    
    try:
        db_produto = models.Produto(nome=produto.nome,
                                    preco=produto.preco,
                                    descricao=produto.descricao, 
                                    tipo=produto.tipo)
        db.add(db_produto)
        db.commit()
        db.refresh(db_produto)
    except IntegrityError:
        #verifica se o produto já foi adicionado no banco de dados
        raise HTTPException(status_code=400, detail="Produto já foi adicionado")
    return db_produto
        

def pedir_produto(db: Session, pedido: schemas.PedidoCreate):
    db_pedido = models.Pedido(nome_produto=pedido.nome_produto)
    
    pedido = db.query(models.Pedido).filter(models.Pedido.nome_produto == db_pedido.nome_produto).first()
    
    if pedido is not None:
        raise HTTPException(status_code=400, detail="Produto já pedido")
    
    try:
        db.add(db_pedido)
        db.commit()
        db.refresh(db_pedido)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return db_pedido
