import re
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from fastapi import HTTPException

try:
    from db import models, schemas
except ImportError:
    from cardapio.db import models, schemas

def get_produto(db: Session, nome_produto: str):
    return db.query(models.Produto).filter(models.Produto.nome == nome_produto).first()

def delete_pedidos(db: Session):
    db.query(models.Pedido).delete()
    db.commit()

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
    if not produto.descricao:
        raise HTTPException(status_code=400, detail="A descrição não pode ser vazia")
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
    
def delete_produto(db: Session, nome_produto: str):
    produto = get_produto(db, nome_produto)
    
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não existe")
        
    db.delete(produto)
    db.commit()

def get_produtos_tipos(db: Session, tipo: int):
    return db.query(models.Produto).filter(models.Produto.tipo == tipo).all()

def pedir_produto(db: Session, nome_produto: str):
    produto = get_produto(db, nome_produto)
    
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não existe")
    
    pedido_atual = db.query(models.Pedido).filter(models.Pedido.id_produto == produto.id).first()
    
    try:
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
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
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
    pedidos = db.query(models.Pedido).all()
    produtos_pedidos: list[schemas.Produto] = []
    preco_total: float = 0

    if len(pedidos) == 0:
        raise HTTPException(status_code=400, detail="Lista de pedido vazia") 

    for pedido_db in pedidos:
        produto = schemas.Produto(id=pedido_db.produto.id,
                                nome=pedido_db.produto.nome,
                                descricao=pedido_db.produto.descricao,
                                preco=pedido_db.produto.preco,
                                tipo=pedido_db.produto.tipo)
        pedido = schemas.Pedido(id_produto=pedido_db.id_produto,
                                quantidade=pedido_db.quantidade,
                                produto=produto)
        preco_total += produto.preco * pedido.quantidade
    
    delete_pedidos(db)
    return preco_total
        
    
        
            
    