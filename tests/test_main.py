from fastapi.testclient import TestClient

from cardapio.main import app

client = TestClient(app)


def test_listar_produtos():
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
    print(response)
    assert response.status_code == 200
