from pydantic import BaseModel


class ProdutoBase(BaseModel):
    nome: str
    descricao: str
    preco: int
    tipo: int


class ProdutoCreate(ProdutoBase):
    pass


class Produto(ProdutoBase):
    id: int

    class Config:
        orm_mode = True


class PedidoBase(BaseModel):
    produto_id: int


class PedidoCreate(PedidoBase):
    pass

class Pedido(PedidoBase):
    id: int
    product: Produto

    class Config:
        orm_mode = True
