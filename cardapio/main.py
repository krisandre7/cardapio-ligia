from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


try:
    from db import models, schemas
    from db.database import SessionLocal, engine
    from db import crud
except ImportError:
    from cardapio.db import models, schemas, crud
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

@app.post("/produtos/")
def cadastrar_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    crud.cadastrar_produto(db, produto)
    return {"message": "Produto criado com sucesso"}

@app.put("/produtos/")
def update_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    try:
        crud.update_produto(db, produto)
    except HTTPException as e:
        raise e
    return {"message": "Produto atualizado com sucesso!"}

@app.get("/produtos/{tipo}", response_model=list[schemas.Produto])
def listar_produtos_tipo(tipo: int, db: Session = Depends(get_db)):
    if tipo != 0 and tipo != 1:
        return HTTPException(status_code=400, detail="Número inválido. Por favor coloque 0 ou 1")
    produtos = crud.get_produtos_tipos(db, tipo)
    return produtos

@app.post("/pedido/{nome_produto}")
def pedir_produto(nome_produto: str, db: Session = Depends(get_db)):
    try:
        crud.pedir_produto(db, nome_produto)
    except HTTPException as e:
        raise e
    return JSONResponse(status_code=200, content={"message": "Produto pedido com sucesso!"})

@app.get("/pedido/")
def efetuar_pedido(db: Session = Depends(get_db)):
    preco_total: float = 0
    produtos_pedidos: list[schemas.Produto] = []
    try:
        preco_total = crud.efetuar_pedido(db)
    except HTTPException as e:
        raise e 
    return {"preco_total": preco_total, "produtos_pedidos": produtos_pedidos}
        
            

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=5000, log_level="info", reload=True)