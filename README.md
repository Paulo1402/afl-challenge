# AFL Challenge - Backend

## Iniciar o projeto

Para executar o projeto é necessário as seguintes etapas:

- Criar um arquivo `.env` na raiz do projeto com as seguintes variáveis:
```SECRET_KEY=afl-challenge
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=afl-challenge
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

- Instalar Python 3.10+: `sudo apt install python3 python3-pip`
- Instalar o docker: `sudo apt install docker.io`
- Criar um ambiente virtual: `python3 -m venv venv`
- Ativar o ambiente virtual: `. venv/bin/activate`
- Instalar as dependências do projeto: `pip install -r requirements.txt`

- Subir o container do banco de dados: `docker-compose up -d`
- Executar o projeto: `fastapi dev`
- Acessar a documentação da API: `http://localhost:8000/docs`

## Tecnologias
- Fastapi
- Pydentic
- Peewee
- Docker