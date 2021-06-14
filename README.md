[![author](https://img.shields.io/badge/author-brunovn-red.svg)](www.linkedin.com/in/brunovn) 
[![python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/release/python-365/) 
[![GPLv3 license](https://img.shields.io/badge/License-MIT-blue.svg)]
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/bruno154/Data_Science_Python/issues)

# WineClassifierApp
Repositório destinado à abrigar os arquivos necessarios para o desenvolvimento 
do WineClassifierApp.

## Descrição:
 O app será desenvolvido a partir de dados extraídos, através de web scrapping do site www.wine.com. O objetivo é construir um classificador retorne a probabilidade de um determinado vinho ser avaliado pelos seus clientes.

## Estrutura do Projeto.
O projeto será composto por dois diretórios principais, conforme abaixo:

* app: scripts e outros aqruivos necessários para rodar o app.

* notebooks: conterá notebooks com análises e codigos para cada etapa do projeto. 

## Passos do projeto.

* [X] Analisar codigo HTML da pagina e traçar estratégia de scrapping. 
* [X] Realizar a extração dos dados conforme estratégia.
* [X] Armazenar os dados em um banco de dados relacional Postgres.
* [X] Performar EDA, teste estatísticos e determinar as variáveis do modelo.
* [X] Desenvolver o app e realizar o deploy com a lib streamlit.

## Getting Started

### Installation
Com o conteúdo da pasta app no diretório desejado. Instalar os requirements no seu ambiente de desenvolvimento conforme abaixo:
 ```bash
 $ pip install requirements.txt
 ```  
Ativar o app com o comando abaixo:.
```bash
$ streamlit run app.py
```
