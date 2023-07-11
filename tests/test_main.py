from fastapi.testclient import TestClient

from cardapio.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Salve Salve Família"}
    
def test_create_produto():
    response = client.delete('/')
    response = client.post(
        "/produtos/",
        json={
            "nome": "Coca-Cola",
            "descricao": "Refrigerante de cola",
            "preco": 5.0,
            "tipo": 1
        },
    )
    assert response.status_code == 200
    
def test_pedir_produto():
    client.delete('/')
    client.post(
        "/produtos/",
        json={
            "nome": "Coca-Cola",
            "descricao": "Refrigerante de cola",
            "preco": 5.0,
            "tipo": 1
        },
    )
    
    response = client.post("/pedido/Coca-Cola")
    assert response.status_code == 200
    
def test_pedir_produto_nao_existe():
    client.delete('/')
    response = client.post("/pedido/Coca-Cola")
    assert response.status_code == 404
    
def test_pedir_produto_existente():
    client.delete('/')
    client.post(
        "/produtos/",
        json={
            "nome": "Coca-Cola",
            "descricao": "Refrigerante de cola",
            "preco": 5.0,
            "tipo": 1
        },
    )
    client.post("/pedido/Coca-Cola")
    response = client.post("/pedido/Coca-Cola")
    assert response.status_code == 400
    
