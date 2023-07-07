#!/bin/bash
#Subir o ambiente do Banco de Dados Relacional MySQL
result=$(docker container ls -a | grep mysql-ligia)
container_mysql='mysql-ligia'

# verificar se o container mysql-ligia já foi criado
if [[ "$result" == *"$container_mysql"* ]]; 
then
    # apenas inicializa o container caso já esteja criado
    docker container start mysql-ligia
else
    # cria o container caso não foi criado
    docker run --name mysql-ligia  -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root -e MYSQL_USER=prometheus -e MYSQL_PASSWORD=12345 -e MYSQL_DATABASE=prometheus-mysql -d mysql:8.0.33
fi

docker container run --name cardapio-mysql -v $(pwd):/apps -it -p 5000:5000  cardapio-ligia-backend

# # --name    nome do container
# # -v        mapear volume local:dentro_container
# # -it       modo iterativo, ou seja, permite entrar no container em modo console
# # -p        externalizar uma porta para acesso internamente ao container

docker container rm -f cardapio-mysql

docker container stop mysql-ligia

# rm -f     apaga um container (-f )

# Fonte: https://docs.docker.com/engine/reference/run/