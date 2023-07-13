from fastapi.testclient import TestClient

from cardapio.main import app

client = TestClient(app)

def test_cadastrar_produto():
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
    
def test_cadastrar_produto_nome_invalido():
    response = client.delete('/')
    response = client.post(
        "/produtos/",
        json={
            "nome": "",
            "descricao": "Refrigerante de cola",
            "preco": 5.0,
            "tipo": 1
        },
    )
    
    assert response.status_code == 400

def test_cadastrar_produto_desc_invalido():
    response = client.delete('/')
    response = client.post(
        "/produtos/",
        json={
            "nome": "Coca-Cola",
            "descricao": "",
            "preco": 5.0,
            "tipo": 1
        },
    )
    
    assert response.status_code == 400
    
def test_cadastrar_produto_preco_invalido():
    response = client.delete('/')
    response = client.post(
        "/produtos/",
        json={
            "nome": "Coca-Cola",
            "descricao": "Refrigerante de cola",
            "preco": 0,
            "tipo": 1
        },
    )
    
    assert response.status_code == 400

def test_cadastrar_produto_existente():
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
    response = client.post(
        "/produtos/",
        json={
            "nome": "Coca-Cola",
            "descricao": "Refrigerante de cola",
            "preco": 5.0,
            "tipo": 1
        },
    )
    
    assert response.status_code == 400

def test_atualizar_produto():
    client.delete('/')
    client.post(
        "/produtos/",
        json={
            "nome": "Coca-Cola",
            "descricao": "Refrigrante de cola",
            "preco": 7.0,
            "tipo": 1
        },
    )

    response = client.put(
        "/produtos/",
        json={
            "nome": "Coca-Cola",
            "descricao": "Coca Cola Trincando",
            "preco": 10.0,
            "tipo": 1
        },
    )
    
    assert response.status_code == 200

def test_apagar_produto():
    client.delete("/")
    response = client.post(
        "/produtos/",
        json={
            "nome": "Coca-Cola",
            "descricao": "Refrigerante de cola",
            "preco": 5.0,
            "tipo": 1
        },
    )
    
    response = client.delete("/produtos/Coca-Cola")
    
    assert response.status_code == 200

def test_apagar_produto_inexistente():
    client.delete("/")

    response = client.delete("/produtos/Coca-Cola")
    
    assert response.status_code == 404

def test_listar_produtos_tipo():
    response = client.delete('/')
    response = client.post(
        "/produtos/",
        json = {
            "nome": "arroz",
            "descricao": "alimentos de cesta básica 01",
            "preco": 5.0,
            "tipo": 0
        },
    )
    response = client.post(
        "/produtos/",
        json = {
            "nome": "Coca-Cola",
            "descricao": "Refrigerante de cola",
            "preco": 3.5,
            "tipo": 1
        },
    )

    response = client.get("/produtos/0")
    assert response.status_code == 200

def test_pedir_produto():
    client.delete('/')
    client.post(
        "/produtos/",
        json={
            "nome": "Coca-Cola",
            "descricao": "Coca Cola Trincando",
            "preco": 10.0,
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
            "descricao": "Coca Cola Trincando",
            "preco": 10.0,
            "tipo": 1
        },
    )
    client.post("/pedido/Coca-Cola")
    response = client.post("/pedido/Coca-Cola")
    assert response.status_code == 200
    
def test_remover_pedido():
    client.delete('/')
    client.post(
        "/produtos/",
        json={
            "nome": "Coca-Cola",
            "descricao": "Coca Cola Trincando",
            "preco": 10.0,
            "tipo": 1
        },
    )
    
    response = client.post("/pedido/Coca-Cola")
    response = client.delete("/pedido/Coca-Cola")
    
    assert response.status_code == 200

def test_remover_pedido_produto_inexistente():
    client.delete('/')
    client.post(
        "/produtos/",
        json={
            "nome": "Coca-Cola",
            "descricao": "Coca Cola Trincando",
            "preco": 10.0,
            "tipo": 1
        },
    )
    
    response = client.delete("/pedido/Coca-Cola")
    
    assert response.status_code == 404

def test_remover_pedido_inexistente():
    client.delete('/')
    response = client.delete("/pedido/Coca-Cola")
    
    assert response.status_code == 404