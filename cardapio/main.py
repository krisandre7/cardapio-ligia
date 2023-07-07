from typing import Union

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from db import models, schemas
from db.database import SessionLocal, engine
from db import crud

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

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool

items: list = []

@app.get("/")
def read_root():
    return {"Salve Salve": "Família"}

@app.get("/produto/{produto_id}", response_model=list[schemas.Produto])
def read_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = crud.get_produto(db, produto_id)
    return produto

@app.get("/produtos/", response_model=list[schemas.Produto])
def read_produtos(db: Session = Depends(get_db)):
    produtos = crud.get_produtos(db)
    return produtos

@app.post("/produtos/")
def create_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    crud.create_produto(db, produto)
    return {"message": "Produto criado com sucesso"}

@app.post("/pedido/{nome_produto}")
def pedir_produto(nome_produto: str, db: Session = Depends(get_db)):
    pedido = schemas.PedidoCreate(nome_produto=nome_produto)
    try:
        crud.pedir_produto(db, pedido)
    except HTTPException as e:
        raise e
    return {"message": "Pedido criado com sucesso"}
    

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=5000, log_level="info", reload=True)