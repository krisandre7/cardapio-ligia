import re
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from fastapi import HTTPException

try:
    from db import models, schemas
    from db.schemas import TipoProduto
except ImportError:
    from cardapio.db import models, schemas
    from cardapio.db.schemas import TipoProduto

def get_produto(db: Session, nome_produto: str):
    return db.query(models.Produto).filter(models.Produto.nome == nome_produto).first()

def get_pedido(db: Session):
    return db.query(models.Pedido).all()

def clear_db(db: Session):
    db.query(models.Pedido).delete()
    db.query(models.Produto).delete()
    db.commit()
    return {"message": "Banco de dados limpo"}

def cadastrar_produto(db: Session, produto: schemas.ProdutoCreate):
    #verifica se o produto é vazio
    if re.match(r"\w", produto.nome) is None:
        raise HTTPException(status_code=400, detail="Nome inválido")
    #verifica se a descrição é vazio
    if re.match(r"\w", produto.descricao) is None:
        raise HTTPException(status_code=400, detail="A descrição não pode ser vazia")
    #verifica se o preço é diferente de zero ou negativo
    if produto.preco <= 0:
        raise HTTPException(status_code=400, detail="O valor precisa ser maior que zero")
    
    try:
        db_produto = models.Produto(nome=produto.nome,
                                    preco=produto.preco,
                                    descricao=produto.descricao, 
                                    tipo=int(produto.tipo))
        db.add(db_produto)
        db.commit()
        db.refresh(db_produto)
    except IntegrityError:
        #verifica se o produto já foi adicionado no banco de dados
        raise HTTPException(status_code=400, detail="Produto já foi adicionado")        

def update_produto(db: Session, produto: schemas.ProdutoCreate):
    db_produto = models.Produto(nome=produto.nome, 
                                preco=produto.preco, 
                                tipo=int(produto.tipo), 
                                descricao=produto.descricao)
    produto_atual = db.query(models.Produto).filter(models.Produto.nome == db_produto.nome).first()
    
    if produto_atual is None:
        raise HTTPException(status_code=404, detail="Produto com esse nome não existe.")
    
    produto_atual.descricao = db_produto.descricao
    produto_atual.preco =  db_produto.preco
    produto_atual.tipo = db_produto.tipo
    db.commit()
    db.refresh(produto_atual)
    
def delete_produto(db: Session, nome_produto: str):
    produto = get_produto(db, nome_produto)
    
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não existe")
        
    db.delete(produto)
    db.commit()

def get_produtos_tipos(db: Session, tipo: TipoProduto):
    return db.query(models.Produto).filter(models.Produto.tipo == int(tipo)).all()

def pedir_produto(db: Session, nome_produto: str):
    produto = get_produto(db, nome_produto)
    
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não existe")
    
    pedido_atual = db.query(models.Pedido).filter(models.Pedido.id_produto == produto.id).first()
    
    if pedido_atual is not None:
        pedido_novo = models.Pedido(id_produto=pedido_atual.id_produto,
                                    quantidade=pedido_atual.quantidade + 1,
                                    produto=pedido_atual.produto)
        pedido_atual.quantidade = pedido_novo.quantidade
        db.commit()
        db.refresh(pedido_atual)
    else:
        pedido_novo = models.Pedido(id_produto=produto.id, quantidade=1) 
        db.add(pedido_novo)
        db.commit()
        db.refresh(pedido_novo)
    
def remover_pedido(db: Session, nome_produto: str):
    produto = get_produto(db, nome_produto)
    
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    pedido = db.query(models.Pedido).filter(models.Pedido.id_produto == produto.id).first()
    
    if pedido is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado no pedido")  
    
    db.delete(pedido)
    db.commit()

def efetuar_pedido(db: Session):
    pedidos = get_pedido(db)
    produtos_pedidos: list[schemas.Produto] = []
    preco_total: float = 0

    if len(pedidos) == 0:
        raise HTTPException(status_code=404, detail="Lista de pedido vazia") 

    for pedido_db in pedidos:
        produto = schemas.Produto(id=pedido_db.produto.id,
                                nome=pedido_db.produto.nome,
                                descricao=pedido_db.produto.descricao,
                                preco=pedido_db.produto.preco,
                                tipo=TipoProduto(pedido_db.produto.tipo))
        pedido = schemas.Pedido(id_produto=pedido_db.id_produto,
                                quantidade=pedido_db.quantidade,
                                produto=produto)
        preco_total += produto.preco * pedido.quantidade
    
    db.query(models.Pedido).delete()
    db.commit()
    return preco_total
        
    
        
            
    