[![Lint](https://github.com/Lend-it/Request/actions/workflows/black.yml/badge.svg)](https://github.com/Lend-it/Request/actions/workflows/black.yml) [![SonarCloud analysis](https://github.com/Lend-it/Request/actions/workflows/sonar.yml/badge.svg)](https://github.com/Lend-it/Request/actions/workflows/sonar.yml) [![Commit Linter](https://github.com/Lend-it/Request/actions/workflows/commit-linter.yml/badge.svg)](https://github.com/Lend-it/Request/actions/workflows/commit-linter.yml) [![Application Test](https://github.com/Lend-it/Request/actions/workflows/app-test.yml/badge.svg)](https://github.com/Lend-it/Request/actions/workflows/app-test.yml) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Lend-it_Request&metric=alert_status)](https://sonarcloud.io/dashboard?id=Lend-it_Request)
# Request

Microsserviço responsável pelo sistema de pedidos de empréstimos.

## Ambientes
### Local
**[Disponível na porta 5002.](http://localhost:5002/)**

### Ambiente de homologação
**[Disponível no Heroku](https://lendit-request-homolog.herokuapp.com/)**

### Ambiente de produção
**[Disponível no Heroku](https://lendit-request-prod.herokuapp.com/)**

***
## Colocando no ar localmente

1. Build
```shell
    make build
```
2. Executar
```shell
    make run
```
2.1 Executar em background
```shell
    make run-silent
```
2.2 Buildar e executar
```shell
    make run-build
```
3. Desativar o container
```shell
    make down
```

## Rodando os testes

```shell
    make test
```

## Rodando a cobertura dos testes


```shell
    make cov
```

## Acessando o banco de dados 

```shell
    make check-db
```

## Rodar o linter no código (Black) 

```shell
    make lint
```
