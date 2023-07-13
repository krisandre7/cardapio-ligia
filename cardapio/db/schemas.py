from pydantic import BaseModel
from enum import IntEnum

class TipoProduto(IntEnum):
    comida = 0
    bebida = 1

class ProdutoBase(BaseModel):
    nome: str
    descricao: str
    preco: float
    tipo: TipoProduto


class ProdutoCreate(ProdutoBase):
    pass


class Produto(ProdutoBase):
    id: int

    class Config:
        orm_mode = True


class PedidoBase(BaseModel):
    id_produto: int
    quantidade: int


class PedidoCreate(PedidoBase):
    pass

class Pedido(PedidoBase):
    produto: Produto

    class Config:
        orm_mode = True
