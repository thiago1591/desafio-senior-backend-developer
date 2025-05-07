discussão de decisões

1) Arquitetura modular
Atualmente costumo usar arquitetura modular para os meus projetos. Eu já utilizei no passado uma arquitetura em que existiam pastas para agrupar os arquivos de cada funcionalidade (por exemplo vários services dentro de uma pasta de service) do sistema e conforme o projeto cresceu ficou cada vez mais difícil de manter. Por isso escolhi seguir essa abordagem em que cada módulo tem sua responsabilidade. É uma estrutura simples de entender então acredito que faça sentido até mesmo para projetos menores, pois garante que caso um dia seja preciso escalar, será possível.

2) Sobre as camadas dos módulos
A divisão de camadas que implementei é algo que vejo se tornar um padrão comum em diferentes linguagens.
Por exemplo, o NestJS (framework backend de javascript) usa outras nomenclaturas em relação a minha implementação em fastAPI mas a ideia geral é a mesma

2.1) Uma camada de validação da tipagem dos dados de entrada
2.2) Uma cada de validação mais profunda dos dados de entrada, fazendo validações com o banco
2.3) Um roteador para criar o endpoint que irá apontar para a camada da regra de negócio
2.4) A camada de regra de negócio com a lógica em si
2.5) A camada com a modelagem da estrutura das tabelas, que permite a comunicação com o ORM

Essa abordagem permite uma manutenção mais fácil pois a divisão de responsabilidades fica mais clara
É possível usar um service em outro módulo. Por exemplo, importar um service de findOne do modulo de usuário, sem precisar reimplementar em outro módulo
Fica mais fácil de testar

3) Observabilidade
Decidi implementar um esboço de observabilidade como um bonus, pois em muitos projetos em que trabalhei, após ir para produção, me passavam problemas que o cliente eventualmente reclamava e eu precisava debugar localmente para tentar entender. Por isso atualmente eu sempre que começo um projeoto, implemento observabilidade desde o início pois permite ter infomações do sistema em produção diretamente, o que economiza bastante tempo.

4) segurança

5) Modelagem
Na modelagem da tabela de Document, supus que todo documento pertence a um único usuário (1:N), por conta disso, criei uma tabela do document com user_id em vez de uma tabela de document e outra user_documents.


uvicorn src.main:app --reload

aerich init -t src.database.TORTOISE_ORM 



python -m venv venv
source venv/bin/activate  # No Windows use `venv\Scripts\activate`
pip install -r requirements.txt