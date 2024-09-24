# Ferramenta de Doação de Alimentos (2023)

## Objetivo 
Facilitar a conexão entre ONGs que distribuem alimentos e estabelecimentos dispostos a doar. As ONGs podem se cadastrar e criar pedidos de doação, enquanto os estabelecimentos podem se registrar e atender a esses pedidos.

## Funcionalidades
* Cadastro e login de ONGs e estabelecimentos.
* Criação e atendimento de pedidos de doação.
* Configuração, alteração e exclusão de informações de cadastro.
* Consulta, alteração e exclusão de pedidos de doação e entrega (atendimento dos pedidos).
* Armazenamento dos dados em banco de dados Oracle.

## Funcionamento
* O usuário deverá cadastrar uma conta, inserindo nome, e-mail, senha, CNPJ e um ou mais endereços, além de escolher entre se cadastrar como ONG ou estabelecimento.
* É feita uma validação para garantir a unicidade do e-mail inserido na base de dados e também de que a senha contenha no mínimo 6 caracteres, números e letras maiúsculas e minúsculas, para garantir maior segurança da conta.
* Ao se cadastrar como ONG e realizar o login, é possível cadastrar pedidos, inserindo o produto que deseja pedir e a quantidade.
* Se cadastrando como estabelecimento e realizando login, é possível cadastrar entregas, consultando a lista de pedidos e escolhendo o desejado. Você pode escolher o endereço de mais fácil acesso ao estabelecimento, definir a data de entrega e, se necessário, adicionar observações.
* Ambos os tipos de cadastro tem acesso aos relatórios, onde podem consultar a lista de ONGs e estabelecimentos, endereços, pedidos e entregas.
 
## Tecnologias
* Python
* Oracle DataBase  
* SqlAlchemy
  
## Configuração
* Clone o repositório.
* Preencha o arquivo 'db/config.py' com suas credenciais do Oracle (username, password, server, port, dbname e oracle_client_path).
