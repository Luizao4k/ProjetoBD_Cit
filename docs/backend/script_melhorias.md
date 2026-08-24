## 🔮 Melhorias Futuras

As funcionalidades abaixo não fazem parte do escopo inicial do projeto, mas foram identificadas como evoluções importantes para aumentar a produtividade durante o desenvolvimento, facilitar a manutenção do sistema e tornar a infraestrutura de importação mais robusta.

### Scripts de automação

Implementar scripts auxiliares para automatizar tarefas recorrentes:

* `recriar_banco.py` — remove o banco existente e o recria do zero.
* `verificar_banco.py` — exibe um resumo das tabelas e da quantidade de registros importados.
* `importar_tudo.py` — executa automaticamente toda a sequência de importação respeitando as dependências entre as entidades.
* `popular_banco.py` — gera dados fictícios para testes da API e do frontend.

### Melhorias na importação

Evoluir o subsistema de importação com funcionalidades adicionais:

* Suporte a múltiplos formatos de arquivo (CSV, Excel e futuramente Google Sheets).
* Relatórios mais completos de importação, incluindo tempo de execução, quantidade de registros processados, sucessos e falhas.
* Logs detalhados das alterações realizadas em importações incrementais.
* Possibilidade de reprocessar apenas registros com falha.
* Barra de progresso mais informativa para grandes volumes de dados.
* Validações prévias dos arquivos antes do início da importação.

### Infraestrutura

Melhorar a infraestrutura do projeto com recursos de apoio ao desenvolvimento:

* Centralizar funcionalidades compartilhadas dos scripts em um módulo utilitário para evitar duplicação de código.
* Criar comandos para backup e restauração do banco de dados.
* Adicionar integração futura com sistema de migrações do banco (caso o projeto evolua para PostgreSQL ou outro SGBD).
* Disponibilizar comandos automatizados para preparação completa do ambiente de desenvolvimento.
