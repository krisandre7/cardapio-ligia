from fastapi.testclient import TestClient

from cardapio.main import app

client = TestClient(app)

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
