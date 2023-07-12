from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from fastapi import HTTPException

try:
    from db import models, schemas
except ImportError:
    from cardapio.db import models, schemas

def get_produto(db: Session, id_produto: int):
    return db.query(models.Produto).filter(models.Produto.id == id_produto).first()

def delete_pedidos(db: Session):
    db.query(models.Pedido).delete()
    db.commit()
    return {"message": "Pedidos deletados com sucesso"}

def clear_db(db: Session):
    db.query(models.Pedido).delete()
    db.query(models.Produto).delete()
    db.commit()
    return {"message": "Banco de dados limpo"}

def cadastrar_produto(db: Session, produto: schemas.ProdutoCreate):
    db_produto = models.Produto(nome=produto.nome,
                                preco=produto.preco,
                                descricao=produto.descricao, 
                                tipo=produto.tipo)
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

def update_produto(db: Session, produto: schemas.ProdutoCreate):
    db_produto = models.Produto(nome=produto.nome, 
                                preco=produto.preco, 
                                tipo=produto.tipo, 
                                descricao=produto.descricao)
    produto_antigo = db.query(models.Produto).filter(models.Produto.nome == db_produto.nome).first()
    
    if produto_antigo is None:
        raise HTTPException(status_code=400, detail="Produto com esse nome não existe.")
    
    try: 
        produto_antigo.descricao = db_produto.descricao
        produto_antigo.preco =  db_produto.preco
        produto_antigo.tipo = db_produto.tipo
        db.commit()
        db.refresh(produto_antigo)
    except IntegrityError as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=404, detail="Produto não encontrado")

def get_produtos_tipos(db: Session, tipo: int):
    return db.query(models.Produto).filter(models.Produto.tipo == tipo).all()

def pedir_produto(db: Session, nome_produto: str):
    
    produto = db.query(models.Produto).filter(models.Produto.nome == nome_produto).first()
    
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não existe")
    
    pedido = db.query(models.Pedido).filter(models.Pedido.id_produto == produto.id).first()
    
    if pedido is not None:
        raise HTTPException(status_code=400, detail="Produto já pedido")
    
    db_pedido = models.Pedido(id_produto=produto.id)
    
    try:
        db.add(db_pedido)
        db.commit()
        db.refresh(db_pedido)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return db_pedido

def efetuar_pedido(db: Session):
    pedidos = db.query(models.Pedido).all()
    produtos_pedidos: list[schemas.Produto] = []
    preco_total: float = 0

    if len(pedidos) == 0:
        raise HTTPException(status_code=400, detail="Lista de pedido vazia") 

    for pedido in pedidos:
        produto = schemas.Produto(id=pedido.produto.id,
                                nome=pedido.produto.nome,
                                descricao=pedido.produto.descricao,
                                preco=pedido.produto.preco,
                                tipo=pedido.produto.tipo)
        preco_total += produto.preco
        produtos_pedidos.append(produto)
    
    # delete_pedidos(db)
    return preco_total, produtos_pedidos
        
    
        
            
    