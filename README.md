# Desafio Técnico – Desenvolvedor(a) Back-end Sênior

Bem-vindo(a) ao desafio técnico para a vaga de Pessoa Desenvolvedora Back-end Sênior!

Neste README estão detalhadas todas as informações sobre a minha implementação do desafio

## 📌 Contexto

A Prefeitura do Rio de Janeiro quer oferecer aos cidadãos uma **API de Carteira Digital**, onde os usuários poderão armazenar e gerenciar documentos digitais, consultar e carregar créditos do transporte público e acessar serviços municipais via chatbot.

O desafio é desenvolver uma API para essa carteira digital, simulando as interações do usuário com documentos e transporte público.

## Prévia
Antes de realizar as etapas para rodar o projeto, você pode visualizar a API que está disponível publicamente em:

[https://api.iplan.thiagoandre.dev.br/docs](https://api.iplan.thiagoandre.dev.br/docs)
## Rodando o projeto
### Requisitos
 - Docker instalado
### Comando
```console
docker-compose --profile dev up -d
```
Esse comando irá subir o banco de dados e a API, que estará disponível localmente na porta **8000**

## Documentação
A API está documentada no Swagger, acessando a rota [/docs](http://localhost:8000/docs)

## Estrutura do projeto
```
desafio-senior-backend-developer
├── .github
│   ├── workflows
│   │   ├── ci.yml
├── src
│   ├── user
│   │   ├── router.py
│   │   ├── schemas.py 
│   │   ├── models.py 
│   │   ├── dependencies.py
│   │   ├── config.py 
│   │   ├── exceptions.py
│   │   ├── service.py
│   │   └── utils.py
│   ├── ... (outros módulos)
│   ├── config.py  
│   ├── models.py 
│   ├── database.py  
│   └── main.py
├── tests/
├── requirements
├── .env
├── .gitignore
...
```
A estrutura do projeto segue uma arquitetura modular, onde cada módulo tem algumas camadas. Elas serão explicadas na próxima seção

## Camadas do módulo
   1. `router.py` - é o núcleo de cada módulo com todos os endpoints
   2. `schemas.py` - para os modelos Pydantic (define e valida os dados recebidos e retornados)
   3. `models.py` - modelos do banco de dados
   4. `service.py` - aqui estão as regras de negócio
   5. `dependencies.py` - dependencias do router
   8. `utils.py` - funções de utilitários
   9. `exceptions.py` - excessões específicas do módulo, ex: `DocumentNotFound`


## Testes
Os testes estão no diretórios `tests` na raiz do projeto. Estão implementados tanto testes de unidade quanto teste de integração.

O objetivo dos testes de unidade é testar a regra de negócio de forma completamente isolada. É possível testar cenários específicos, como o caso do teste `test_multiple_recharges_accumulates_correctly` em que é testado várias recargas no cartão de transporte em sequência e verificado se a soma é acumulada corretamente.

Os testes de integração, por outro lado, testam um cenário mais realista. O service não é testado isolado, mas sim junto com a rota e o banco de dados. Foi utilizado o SQlite como banco fake para realização dos testes de integração.

Os testes são executados automaticamente ao enviar um push. Se você quiser rodar manualmente, é necessário rodar os testes de integração separado dos de unidade. 
A variável TESTING=1 serve para impedir que o banco real Postgres inicialize

todo: adicionar explicação para rodar manual


```
├── tests
│   ├── integration
│   │   ├── test_auth.py
│   │   ├── test_documents.py
│   │   ├── test_transport.py
│   │   ├── test_users.py
│   ├── unit
│   │   ├── documents
│   │   │   ├── test_documents_service.py  
│   │   ├── transport
│   │   │   ├── test_transport_service.py
│   │   ├── user
│   │   │   ├── test_user_service.py

```


## 🔹 Funcionalidades

- Autenticação e Gerenciamento de Usuários
    - Cadastro e login de usuários (simples, com e-mail/senha).
    - Uso de tokens JWT para autenticação.
    - CRUD de usuários

- Gestão de Documentos
    - Endpoints para armazenar, listar, atualizar e deletar documentos digitais (exemplo: identidade, CPF, comprovante de vacinação).

- Gestão de Transporte Público
    - Endpoint para buscar os meus cartões de transporte público
    - Endpoint para consultar saldo do passe de transporte público
    - Endpoint para simular recarga e débido do passe
    - Endpoint para ver o histórico de transações

- Integração com Chatbot (Simples)
    - Consultar o saldo do passe pelo bot
    - Ver os meus documentos pelo bot
    - Fazer uma pergunta livre (resposta de perguntas mokadas)
    - Cancelar Cartão (simulado, apenas diz que criou uma solicitação de cancelamento)
    - Salvar documento (iniciado mas não finalizado)

## 🔹 Tecnologias

- FastAPI como framework principal.
- Banco de Dados PostgreSQL 
- ORM Tortoise-ORM
- Ferramenta de migrations Aerich
- PyTest
- OpenAPI para Documentação da API
- GitHub Actions
- Docker

## 🔹 Discussão de decisões

### Escolha das tecnologias
O banco de dados escolhido foi o Postgres. Para o escopo dessa API, a escolha entre o MySQL e Postgres não traria mudanças significativas. Optei pelo Postgres pois é o banco que tenho maior preferência, após realizar um estudo de comparação entre esses 2 bancos, para escrita de um artigo durante a disciplina de Administração de Banco de Dados, na faculdade.
As outras tecnologias usadas foram escolhidas baseadas no que eu tenho mais familiaridade.

### Arquitetura em módulos
Como esse é um projeto simples, talvez não fosse necessário o uso de uma arquitetura modular. Porém, decidi aqui aplicar uma organização que eu usaria para um projeto real. No passado, já tive problemas para manter projetos que não usavam módulos (imagine mais de 80 cruds em uma pasta cruds). Por isso hoje eu sempre utilizo uma abordagem modular. Como é simples de entender a aplicar, faz sentido até mesmo para projetos menores, pois também garante que se um dia precisar, será possível escalar.

### Separação das camadas dos módulos
A separação das camadas, que foi descrita na seção "Camadas do módulo", é algo que funciona muito bem e possui diversas vantagens. É algo que é um padrão usado em diferentes linguagens. Por exemplo, o NestJS (framework backend de Javascript) possui outros termos e nomenclaturas, mas segue uma ideia bem parecida.
Uma camada é responsável por validar e tipar os dados de entrada e saída. Outra define as rotas dos endpoints. Outra define as regras de negócio. Outra define a modelagem da tabela e permite a conexão com o ORM.
As principais vantagens são:
 - 1) manutenabilidade: Abrindo o arquivo de routes, é possível ter uma visão geral e legível das rotas usadas no módulo. Após encontrar a rota que quer da manutenção, é possível facilmente encontrar o service correspondente. Como os arquivos estão em um módulo, não é preciso ficar procurando, por exemplo, o arquivo de service dentro de uma pasta como vários services.
 - 2) testabilidade: separando as responsabilidades em diferentes camadas, fica mais fácil de testar. Por exemplo, é possível criar testes de unidade de forma isolada para os services, pois eles estão separados e não acoplados com as rotas.
 - 3) validações: ter uma camada específica para aplicar validações é muito vantajoso pois não é preciso validar tudo no service. Fica mais fácil de adicionar mais validações, deixando o sistema mais seguro sem prejudicar a legibilidade.

 ### Decisões na modelagem
1) Na modelagem da tabela de Document, supus que todo documento pertence a um único usuário (1:N), por conta disso, criei uma tabela do document com user_id em vez de uma tabela de document e outra user_documents.
2) Decidi modelar a tabela de Document de forma mais simples e genérica dado o escopo desse desafio, mas em um cenário real é possível que os diferentes tipos de documentos tivessem necessidade de campos adicionais
3) Decidi separar o cartão de transporte em uma tabela separada em vez de considerar como um documento na tabela de documentos pois existiria a possibilidade de o cartão de transporte ter mais atributos e funcionalidades específicas no futuro
4) Decidi salvar o saldo como centavos (tipo int) pois é uma boa prática para evitar problemas de arredondamentos em alguams linguagens 

### Sobre a recuperação de senha
Decidi criar um módulo separado para a recuperação de senha pois é o que eu faria em uma API real. Criei alguns endpoints para simular como seria o fluxo e coloquei um comentário onde seria a comunicação com o serviço externo (SMS ou Email) para envio do código de recuperação. Por conta do tempo acabei não finalizando essa módulo. 

### ChatBOT
A funcionalidade do chatbot acredito que seja a funcionalidade desse desafio que poderia seguir diferentes caminhos. Eu achei que seria legal para o contexto desse desafio, usar o chatbot para realizar algumas das funcionalidades dos outros módulos. Também coloquei opção para ele responder uma pergunta, que é a funcionalidade principal requerida no desafio. 
O bot responde perguntas verificando diretamente das perguntas existentes (que estão mokadas). Para uma funcionaldiade real, daria pra usar um banco de dados vetorial para armazenar diferentes perguntas e respostas. Quando o usuário fizesse uma nova pergunta, verificaria a similaridade no espaço vetorial para buscar a resposta mais relevante. Também daria pra usar isso em conjunto com um LLM para passar as respostas mais similares para o contexto do LLM e responder uma resposta ainda mais precisa (técnica de RAG). É algo que eu implementei no meu TCC.


