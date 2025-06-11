# APS_Log_Afazeres
Projeto APS de Lógica da Computação - Linguagem de Tarefas

**Desenvolvido por:** Bruno Falcao

---

## Motivação Sobre a Linguagem 

A ideia da Linguagem de Tarefas surgiu enquanto eu mexia no aplicativo **Notion** para me organizar. Naquele momento, pensei: *"E se existisse uma linguagem simples, direta, quase como pseudocódigo, para escrever e executar listas de tarefas?"*

Foi aí que nasceu a **Linguagem de Tarefas**: uma linguagem minimalista, criada para organizar rotinas e pendências de forma rápida, com comandos claros como `tarefa`, `mostrar`, `feito` e `concluir`.


A linguagem foi criada pra ser uma linguagem simples de organizar tarefas com comandos diretos e intuitivos.

Com ela, dá pra:
- Criar tarefas
- Marcar como concluídas
- Listar todas
- Fazer coisas se alguma condição for verdadeira
- E repetir ações com `enquanto`
---

## Palavras-chave da Linguagem

## Palavras-chave da Linguagem

| Palavra-chave     | Significado                                       |
|-------------------|---------------------------------------------------|
| `tarefa`          | Adiciona uma nova tarefa                          |
| `mostrar`         | Exibe a lista de tarefas com seus status          |
| `concluir`        | Marca uma tarefa como concluída                   |
| `feito`           | Mostra se todas as tarefas foram feitas           |
| `limpar_lista`    | Limpa todas as tarefas da lista                   |
| `se`, `else`      | Estruturas condicionais (if/else)                 |
| `enquanto`        | Laço de repetição (while)                         |


---

## EBNF da Linguagem

```ebnf
programa         ::= comando { comando }

comando          ::= tarefa_cmd
                  | mostrar_cmd
                  | concluir_cmd
                  | feito_cmd
                  | limpar_cmd
                  | se_cmd
                  | enquanto_cmd

tarefa_cmd       ::= "tarefa" STRING
mostrar_cmd      ::= "mostrar"
concluir_cmd     ::= "concluir" STRING
feito_cmd        ::= "feito"
limpar_cmd       ::= "limpar_lista"

se_cmd           ::= "se" "(" expressao ")" bloco ["else" bloco]
enquanto_cmd     ::= "enquanto" "(" expressao ")" bloco

expressao        ::= STRING | NUMBER | ID
                  | expressao OP expressao
                  | "(" expressao ")"

bloco            ::= "{" { comando } "}"

```

## Exemplo de Código

```todo
tarefa "lavar louça"
tarefa "estudar lógica"
tarefa "fazer mercado"

feito

var pendencias int = 2

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
```

## Saida esperada

```
Tarefa adicionada: "lavar louça"
Tarefa adicionada: "estudar lógica"
Tarefa adicionada: "fazer mercado"
Ainda faltam 3 tarefas.
Está tranquilo por enquanto!
Vamos revisar sua lista!
Vamos revisar sua lista!
Tarefa concluída: lavar louça
Tarefa concluída: estudar lógica
Tarefa concluída: fazer mercado
Sim, tudo pronto por agora!
Lista de tarefas foi **resetada** com sucesso!
Lista de tarefas:
```
Curiosidades
- A Linguagem de Tarefas reconhece comandos escritos diretamente em português como tarefa, mostrar, feito, concluir, se, enquanto, entre outros.

- Se você tentar adicionar mais de 5 tarefas pendentes, a linguagem te impede e ainda dá uma bronca:

  "Não posso adicionar mais tarefas. Você já está com muitas, coitado!"

Esse limite de 5 tarefas foi escolhido porque achei que um aluno do Insper com 5 disciplinas já teria tarefas demais pra se organizar num só dia 

- Foi implementada 100% em Python, com parsing manual e execução direta dos comandos.


## Como Compilar / Executar

A linguagem **Linguagem de Tarefas** é interpretada diretamente em **Python**, utilizando o compilador da disciplina **Lógica da Computação — versão 2.4**, estendido para suportar comandos específicos de organização de tarefas.

### ✅ Passos:

1. Escreva seu código em um arquivo com a extensão `.todo` (exemplo: `teste.todo`)
2. Execute o interpretador com o seguinte comando no terminal:

```bash
python Projeto_ToDoLang.py teste.todo

