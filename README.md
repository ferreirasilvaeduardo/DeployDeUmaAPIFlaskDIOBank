# DIO Bank API

## Visão Geral
DIO Bank API é uma aplicação desenvolvida com Flask para gerenciar operações bancárias. Esta API permite criar usuários, gerenciar contas e realizar transações financeiras.

## Funcionalidades
- Criação de usuários
- Gerenciamento de contas bancárias
- Realização de transações financeiras
- Consulta de saldo e extrato

## Tecnologias Utilizadas
- Python
- Flask
- SQLAlchemy
- Pytest

## Instalação

### Pré-requisitos
- Python 3.8+
- Virtualenv

### Passos para Instalação
1. Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/dio_bank.git
    cd dio_bank
    ```

2. Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Configure o banco de dados:
    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

## Uso
Para iniciar a aplicação, execute:
```bash
flask run
```
A API estará disponível em `http://127.0.0.1:5000/`.

### Endpoints Principais
- `POST /users`: Cria um novo usuário
- `GET /users/<id>`: Retorna informações de um usuário
- `POST /accounts`: Cria uma nova conta bancária
- `GET /accounts/<id>`: Retorna informações de uma conta bancária
- `POST /transactions`: Realiza uma transação financeira
- `GET /accounts/<id>/balance`: Retorna o saldo de uma conta bancária
- `GET /accounts/<id>/statement`: Retorna o extrato de uma conta bancária

## Testes
Para rodar os testes, execute:
```bash
pytest
```

## Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

### Passos para Contribuir
1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença
Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.