# APS_Log_Afazeres
Projeto APS de Lógica da Computação - Linguagem de Tarefas

**Desenvolvido por:** Bruno Falcao

---

## Motivação Sobre a Linguagem 

A ideia da ToDoLang surgiu enquanto eu mexia no aplicativo **Notion** para me organizar. Naquele momento, pensei: *"E se existisse uma linguagem simples, direta, quase como pseudocódigo, para escrever e executar listas de tarefas?"*

Foi aí que nasceu a **ToDoLang**: uma linguagem minimalista, criada para organizar rotinas e pendências de forma rápida, com comandos claros como `tarefa`, `mostrar`, `feito` e `concluir`.


A linguagem foi criada pra ser uma linguagem simples de organizar tarefas com comandos diretos e intuitivos.

Com ela, dá pra:
- Criar tarefas
- Marcar como concluídas
- Listar todas
- Fazer coisas se alguma condição for verdadeira
- E repetir ações com `enquanto`
---

## Palavras-chave da Linguagem

## 🔑 Palavras-chave da Linguagem

| Palavra-chave     | Significado                                       |
|-------------------|---------------------------------------------------|
| `tarefa`          | Adiciona uma nova tarefa                          |
| `mostrar`         | Exibe a lista de tarefas com seus status          |
| `concluir`        | Marca uma tarefa como concluída                   |
| `feito`           | Mostra se todas as tarefas foram feitas           |
| `limpar_lista`    | Limpa todas as tarefas da lista                   |
| `se`, `else`      | Estruturas condicionais (if/else)                 |
| `enquanto`        | Laço de repetição (while)                         |
| `Println(...)`    | Imprime texto ou resultado de uma expressão       |
| `Scan()`          | Lê um número do usuário                           |
| `var`             | Declara uma variável com tipo                     |
| `func`            | Declara uma função                                |
| `return`          | Retorna um valor de dentro de uma função          |
| `true`, `false`   | Literais booleanos                                |
| `+`, `-`, `*`, `/`| Operadores aritméticos                            |
| `==`, `>`, `<`    | Operadores relacionais                            |
| `&&`, `||`, `!`   | Operadores lógicos booleanos                      |

---

## EBNF da Linguagem

```ebnf
<programa>       ::= { <comando> '\n' }

<comando>        ::= "tarefa" <string>
                  | "mostrar"
                  | "concluir" <string>
                  | "feito"
                  | "limpar_lista"
                  | <comando_controle>
                  | <atribuicao>
                  | <funcao>
                  | <print>

<comando_controle> ::= "se" <expressao> <bloco> [ "else" <bloco> ]
                     | "enquanto" <expressao> <bloco>

<atribuicao>     ::= "var" <ident> <tipo> [ "=" <expressao> ]
                  | <ident> "=" <expressao>

<print>          ::= "Println" "(" <expressao> ")"

<funcao>         ::= "func" <ident> "(" [ <parametros> ] ")" [ <tipo> ] <bloco>

<bloco>          ::= '{' { <comando> '\n' } '}'

<expressao>      ::= <termo> { ("+"|"-"|"||") <termo> }

<termo>          ::= <fator> { ("*"|"/"|"&&") <fator> }

<fator>          ::= <numero> | <string> | <bool> | <ident> | "Scan()" | "(" <expressao> ")"

<tipo>           ::= "int" | "bool" | "string"
<ident>          ::= [a-zA-Z_][a-zA-Z0-9_]*
<string>         ::= "\"" { caractere } "\""
<numero>         ::= [0-9]+
<bool>           ::= "true" | "false"
```

## Exemplo de Código

tarefa "lavar louça"
tarefa "estudar lógica"
tarefa "fazer mercado"

feito

var pendencias int = 3

se (pendencias > 2) {
  Println("Você tem muitas pendências ainda!")
} else {
  Println("Está tranquilo por enquanto!")
}

var contador int = 0
enquanto (contador < pendencias) {
  Println("Vamos revisar sua lista!")
  contador = contador + 1
}

concluir "lavar louça"
concluir "estudar lógica"
concluir "fazer mercado"

feito

limpar_lista
mostrar

## Saida esperada


Tarefa adicionada: "lavar louça"
Tarefa adicionada: "estudar lógica"
Tarefa adicionada: "fazer mercado"
Ainda faltam 3 tarefas.
Você tem muitas pendências ainda!
Vamos revisar sua lista!
Vamos revisar sua lista!
Vamos revisar sua lista!
Tarefa concluída: lavar louça
Tarefa concluída: estudar lógica
Tarefa concluída: fazer mercado
Sim, tudo pronto por agora!
Lista de tarefas foi **resetada** com sucesso!
Lista de tarefas:
- lavar louça ✅
- estudar lógica ✅
- fazer mercado ✅

🤔 Curiosidades
- A ToDoLang reconhece comandos escritos diretamente em português como tarefa, mostrar, feito, concluir, se, enquanto, entre outros.

- Se você tentar adicionar mais de 5 tarefas pendentes, a linguagem te impede e ainda dá uma bronca:

  "Não posso adicionar mais tarefas. Você já está com muitas, coitado!"

Esse limite de 5 tarefas foi escolhido porque achei que um aluno do Insper com 5 disciplinas já teria tarefas demais pra se organizar num só dia 😅

- Foi implementada 100% em Python, com parsing manual e execução direta dos comandos.


## 🛠️ Como Compilar / Executar

A linguagem **ToDoLang** é interpretada diretamente em **Python**, utilizando o compilador da disciplina **Lógica da Computação — versão 2.4**, estendido para suportar comandos específicos de organização de tarefas.

### ✅ Passos:

1. Escreva seu código em um arquivo com a extensão `.todo` (exemplo: `teste.todo`)
2. Execute o interpretador com o seguinte comando no terminal:

```bash
python Projeto_ToDoLang.py teste.todo

