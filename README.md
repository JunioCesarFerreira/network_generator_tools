# Network Generator Tools

*Tools to generate relational graphs or complex networks.*

## Sobre o repositório

Neste repositório estão alguns scripts Python uteis para gerar grafos ou redes complexas.

As ferramentas deste repositório são desenvolvidas para gerar entradas que podem ser visualizadas com [NetViewJS](https://github.com/JunioCesarFerreira/NetViewJS).

## Como usar

Todo script deste repositório deve ser copiado e executado no diretório onde esteja o arquivo de interesse de análise. 


## Scripts

`docker-analysis.py`: Realiza análise de um **docker-compose** e monta um grafo onde os vértices são os contêiners e suas ligações indicam se estão na mesma **rede docker**.

`sql-tables-analysis.py`: Realiza análise de relações entre tabelas em scripts **SQL**. Monta grafo direcionado onde os vértices são as tabelas e as arestas indicam relações.

`go-dependencies`: Realiza análise de relações de dependências entre *packages* em um projeto **Go**. Monta grafo direcionado onde os vértices são os *packages* e as arestas indicam as dependências.


## Contribuições

Contribuições são bem-vindas!

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE.md](https://github.com/JunioCesarFerreira/network_generator_tools/blob/main/LICENSE) para detalhes.

