# APS_Log_Afazeres
Projeto APS de Lógica da Computação - Linguagem de Tarefas

**Desenvolvido por:** Bruno Falcao

---

## Sobre a Linguagem

A linguagem foi criada pra ser uma linguagem simples de organizar tarefas com comandos diretos e intuitivos.

Com ela, dá pra:
- Criar tarefas
- Marcar como concluídas
- Listar todas
- Fazer coisas se alguma condição for verdadeira
- E até repetir ações com `enquanto`!

Simples, funcional e **Turing completa**

---

## Palavras-chave da Linguagem

| Palavra-chave | Para que serve |
|:---|:---|
| `tarefa` | Adiciona uma tarefa nova |
| `prioridade` | Marca a tarefa como `alta` ou `normal` |
| `prazo` | Define uma data ou limite |
| `status` | Permite criar a tarefa já como `concluida` ou `pendente` |
| `concluir` | Marca uma tarefa como feita |
| `mostrar` | Lista todas as tarefas criadas |
| `se` | Executa um bloco se uma condição for verdadeira |
| `enquanto` | Repete um bloco enquanto uma condição for verdadeira |
| `{` `}` | Agrupa vários comandos dentro de blocos |

---

## EBNF da Linguagem

```ebnf
programa ::= { comando };

comando ::= comando_tarefa
          | comando_concluir
          | comando_mostrar
          | comando_se
          | comando_enquanto;

comando_tarefa ::= 'tarefa' STRING (prioridade | prazo | tarefa_booleana)?;

prioridade ::= 'prioridade' ('alta' | 'normal');

prazo ::= 'prazo' STRING;

tarefa_booleana ::= 'status' ('concluida' | 'pendente');

comando_concluir ::= 'concluir' STRING;

comando_mostrar ::= 'mostrar';

comando_se ::= 'se' STRING bloco;

comando_enquanto ::= 'enquanto' STRING bloco;

bloco ::= '{' { comando } '}';
```

## Exemplo de Código

tarefa "Estudar para APS"
tarefa "Enviar e-mail" status concluida

se "Estudar para APS está pendente" {
  concluir "Estudar para APS"
}

enquanto "ainda tem tarefa pendente" {
  mostrar
}


