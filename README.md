# Request

Microsserviço responsável pelo sistema de pedidos de empréstimos.

## Colocando no ar

Com o Docker e Docker-Compose instalados, basta apenas utilizar os comandos:

```shell
    sudo docker-compose -f docker-compose-dev.yml up --build
```

## Rodando os testes

Com o Docker e Docker-Compose instalados, basta apenas utilizar os comandos:  

```shell
    sudo docker-compose -f docker-compose-dev.yml run rating python manage.py test
```
