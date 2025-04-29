# APS_Log_Afazeres
Projeto APS de Lógica da Computação - Linguagem de Tarefas

**Desenvolvido por:** Bruno Falcao

---

## Sobre a Linguagem

A linguagem foi criada para ser uma linguagem simples para montar listas de tarefas.  
A ideia é ajudar a organizar a vida de alguem desorganizado mostrando uma lista de afazeres.

Com poucos comandos, você pode adicionar tarefas, marcar quando terminar e listar tudo que tem pra fazer.

---

## Palavras-chave da Linguagem

| Palavra-chave | Para que serve |
|:---|:---|
| `tarefa` | Cria uma nova tarefa |
| `prioridade` | Define se a tarefa é mais importante (`alta`) ou normal |
| `prazo` | Coloca uma data limite para a tarefa |
| `concluir` | Marca uma tarefa como feita |
| `mostrar` | Mostra todas as tarefas registradas |

---

## O que tem de diferente

Além de criar tarefas normais, na linguagem também dá pra já criar uma tarefa que nasce como **concluída** ou **pendente**.

Isso ajuda a registrar coisas que já foram feitas, sem precisar ficar mandando `concluir` depois.

---

## EBNF da Linguagem

```ebnf
programa ::= { comando };

comando ::= comando_tarefa
          | comando_concluir
          | comando_mostrar;

comando_tarefa ::= 'tarefa' STRING (prioridade | prazo | tarefa_booleana)?;

prioridade ::= 'prioridade' ('alta' | 'normal');

prazo ::= 'prazo' STRING;

tarefa_booleana ::= 'status' ('concluida' | 'pendente');

comando_concluir ::= 'concluir' STRING;

comando_mostrar ::= 'mostrar';
