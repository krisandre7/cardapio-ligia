from pydantic import BaseModel


class ProdutoBase(BaseModel):
    nome: str
    descricao: str
    preco: float
    tipo: int


class ProdutoCreate(ProdutoBase):
    pass


class Produto(ProdutoBase):
    id: int

    class Config:
        orm_mode = True


class PedidoBase(BaseModel):
    nome_produto: str


class PedidoCreate(PedidoBase):
    pass

class Pedido(PedidoBase):
    id: int
    produto: Produto

    class Config:
        orm_mode = True
