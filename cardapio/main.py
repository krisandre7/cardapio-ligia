from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


try:
    from db import models, schemas
    from db.database import SessionLocal, engine
    from db.schemas import TipoProduto
    from db import crud
except ImportError:
    from cardapio.db import models, schemas, crud
    from cardapio.db.schemas import TipoProduto
    from cardapio.db.database import SessionLocal, engine

# Configuração de acesso ao Banco de Dados
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Disponibiliza a instancia da classe de acesso ao banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

origins = ["http://0.0.0.0:5000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.delete("/")
def clear_db(db: Session = Depends(get_db)):
    return crud.clear_db(db)

@app.get("/pedido/")
def get_pedido(db: Session = Depends(get_db)):
    pedido = crud.get_pedido(db)
    return pedido

@app.post("/produtos/")
def cadastrar_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    try:
        crud.cadastrar_produto(db, produto)
    except  HTTPException as e:
        raise e
    return JSONResponse(status_code=200, content={"message": "Produto adicionado com sucesso"})

@app.put("/produtos/")
def update_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    try:
        crud.update_produto(db, produto)
    except HTTPException as e:
        raise e
    return {"message": "Produto atualizado com sucesso!"}

@app.delete("/produtos/{nome_produto}")
def apagar_produto(nome_produto: str, db: Session = Depends(get_db)):
    try:
        crud.delete_produto(db, nome_produto)
    except HTTPException as e:
        raise e
    return {"message": "Produto apagado com sucesso!"}

@app.get("/produtos/{tipo}", response_model=list[schemas.Produto])
def listar_produtos_tipo(tipo: TipoProduto, db: Session = Depends(get_db)):
    produtos = crud.get_produtos_tipos(db, tipo)
    return produtos
   
@app.post("/pedido/{nome_produto}")
def pedir_produto(nome_produto: str, db: Session = Depends(get_db)):
    try:
        crud.pedir_produto(db, nome_produto)
    except HTTPException as e:
        raise e
    return JSONResponse(status_code=200, content={"message": "Produto pedido com sucesso!"})

@app.delete("/pedido/{nome_produto}")
def remover_pedido(nome_produto: str, db: Session = Depends(get_db)):
    try:
        crud.remover_pedido(db, nome_produto)
    except HTTPException as e:
        raise e
    return JSONResponse(status_code=200, content={"message": "Produto removido do pedido com sucesso!"})

@app.post("/pedido/")
def efetuar_pedido(db: Session = Depends(get_db)):
    preco_total: float = 0
    try:
        preco_total = crud.efetuar_pedido(db)
    except HTTPException as e:
        raise e 
    return {"preco_total": preco_total}
        
            

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=5000, log_level="info", reload=True)