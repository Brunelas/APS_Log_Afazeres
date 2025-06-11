import sys
import re

dict_types = {
    "int": "INT",
    "string": "STR",
    "bool": "BOOL"
}

todo_tasks = []  # Lista de tarefas (simples) com dicionários

class PrePro:
    def filter(source):
        pattern = r'//.*|/\*.*?\*/'
        source = re.sub(pattern, '', source)
        source = re.sub(r'\n\s*\n', '\n', source)
        return source

class SymbolTable:
    def __init__(self,parent = None):
        self.table = {}
        self.parent = parent
        
    def set(self, key, value):
        if key in self.table:
            if self.table[key][1] == value[1]:
                self.table[key] = value
            else:
                raise Exception(f"Type mismatch: {self.table[key]} {value[1]}")
        elif self.parent is not None:
            self.parent.set(key, value)
        else:
            raise Exception(f"Variable {key} not declared")
        if key in self.table.keys():
            if self.table[key] == None:
                if self.parent == None:
                    raise Exception(f"Variable {key} not declared")
                else:
                    self.parent.set(key,value)            
            else:
                if(value[1] == self.table[key][1]):
                    self.table[key] = value
                else:
                    raise Exception(f"Type mismatch: {self.table[key]} {value[1]}")
        else:
            if self.parent == None:
                raise Exception(f"Variable {key} not declared")
            else:
                self.parent.set(key,value)

    def get(self, key):
        if key in self.table.keys():
            value_entry = self.table[key]
            if value_entry[0] is None:
                raise Exception(f"Variable '{key}' declared but not assigned")
            return value_entry
        elif self.parent is not None:
            return self.parent.get(key)
        else:
            raise Exception(f"Undefined variable: {key}")

    
    def create(self,key,value):
        if(key in self.table.keys()):
            raise Exception(f"Variable Already Declared")
        self.table[key] = value

class Node:
    def __init__(self,value,children):
        self.value = value
        self.children = children
    def Evaluate(self,symbolTable):
        pass

class Statements(Node):
    def __init__(self):
        self.statements = []

    def Evaluate(self, symbolTable):
        for statement in self.statements:
            statement.Evaluate(symbolTable)

class Identifier(Node):
    def __init__(self, value):
        self.value = value

    def Evaluate(self, symbolTable):
        if self.value == "tarefas_pendentes":
            pendentes = sum(1 for t in todo_tasks if not t["feito"])
            return (pendentes, "INT")
        return symbolTable.get(self.value)


class VarDec(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, symbolTable):
        var_type = None
        initial_value = None

        if len(self.children) == 2:
            value_node = self.children[0]
            type_name = self.children[1]
            var_type = dict_types.get(type_name, type_name)
            evaluated_value = value_node.Evaluate(symbolTable)

            if evaluated_value[1] != var_type:
                raise Exception(f"Type mismatch: {evaluated_value[1]} and {var_type}")

            initial_value = evaluated_value
        else:
            type_name = self.children[0]
            var_type = dict_types.get(type_name, type_name)
            initial_value = (None, var_type)

        symbolTable.create(self.value.value, (initial_value[0], var_type, False))

class Assigment(Node):
    def __init__(self, value,children):
        self.value = value
        self.children = children
    def Evaluate(self,symbolTable):
        symbolTable.set(self.value.value, self.children.Evaluate(symbolTable))

class Print(Node):
    def __init__(self,value,children):
        self.value = value
        self.children = children
    def Evaluate(self, symbol_table):
        value = self.children.Evaluate(symbol_table)
        if value[1] == "BOOL":
            print(f"{str(value[0]).lower()}")
        else:
            print(f"{value[0]}")

class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    def Evaluate(self,symbolTable):
        left = self.children[0].Evaluate(symbolTable)
        right = self.children[1].Evaluate(symbolTable)
        if self.value == "+":
            if(((left[1] in ["INT","STR","BOOL"]) and (right[1] in ["INT","STR","BOOL"]))):
                if(left[1] == "STR" or right[1] == "STR"):
                    if(right[1]=="BOOL"):
                        return (str(left[0]) + str(right[0]).lower(),"STR")
                    elif(left[1]=="BOOL"):
                        return (str(left[0]).lower()+ right[0],"STR")
                    return (str(left[0]) + str(right[0]),"STR")
                return (left[0] + right[0],"INT")
            else:
                raise Exception(f"Operation PLUS Invalid can't operate {left[1]} and {right[1]}")
        elif self.value == "-":
            if(((left[1]=="INT" and right[1]=="INT"))):
                return (left[0] - right[0],"INT")
            else:
                raise Exception(f"Operation MINUS Invalid can't operate {left[1]} - {right[1]}")
        elif self.value == "*":
            if(left[1]=="INT" and right[1]=="INT"):
                return (left[0] * right[0],"INT")
            else:
                raise Exception(f"Operation MULT Invalid can't operate {left[1]} and {right[1]}")
        elif self.value == "/":
            if(left[1]=="INT" and right[1]=="INT"):
                return (left[0] // right[0],"INT")
            else:
                raise Exception(f"Operation DIV Invalid can't operate {left[1]} and {right[1]}")
        elif self.value == "&&":
            if(left[1]=="BOOL" and right[1]=="BOOL"):
                return (left[0] and right[0],"BOOL")
            else:
                raise Exception(f"Operation AND Invalid can't operate {left[1]} and {right[1]}")
        elif self.value == "||":
            if(left[1]=="BOOL" and right[1]=="BOOL"):
                return (left[0] or right[0],"BOOL")
            else:
                raise Exception(f"Operation OR Invalid can't operate {left[1]} and {right[1]}")
        elif self.value == "==":
            if(left[1] != right[1]):
                raise Exception(f"Operation with incompatible Types can't operate {left[1]} and {right[1]}")
            return (left[0] == right[0],"BOOL")
        elif self.value == ">":
            if(left[1] in ["INT","STR"] and right[1] in ["INT","STR"]):
                return (left[0] > right[0],"BOOL")        
            else:
                raise Exception(f"Operation BIGGER Invalid can't operate ${left[1]} and ${right[1]}")
        elif self.value == "<":
            if(left[1] in ["INT","STR"] and right[1] in ["INT","STR"]):
                return (left[0] < right[0],"BOOL")        
            else:
                raise Exception(f"Operation LESS Invalid can't operate ${left[1]} and ${right[1]}")
        else:
            raise Exception("Invalid BinOp Node")
        
class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    def Evaluate(self,symbolTable):
        number = self.children[0].Evaluate(symbolTable)
        if self.value == "-":
            if(number[1]=="INT"):
                return (-number[0],"INT")
            else:
                raise Exception(f"Operation UNOP MINUS Invalid can't operate ${number[1]}")
        elif self.value =="+":
            if(number[1]=="INT"):
                return (+number[0],"INT")
            else:
                raise Exception(f"Operation UNOP PLUS Invalid can't operate ${number[1]}")
        elif self.value =="!":
            if(number[1]=="BOOL"):
                return (not number[0],"BOOL")
            else:
                raise Exception(f"Operation UNOP NOT Invalid can't operate ${number[1]}")
        else:
            raise Exception("Invalid UnOp Node")

class IntVal(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    def Evaluate(self,symbolTable):
        return (int(self.value),"INT")
    
class BoolVal(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    def Evaluate(self, symbolTable):
        return (self.value,"BOOL")

class StrVal(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    def Evaluate(self, symbolTable):
        return (self.value,"STR")

class While(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    def Evaluate(self,symbolTable):
        typeOfOperation = self.children[0].Evaluate(symbolTable)
        if typeOfOperation[1] != "BOOL":
            raise Exception(f"Operation with incompatible Types can't operate FOR with {typeOfOperation}")
        while typeOfOperation[0]:
            self.children[1].Evaluate(symbolTable)
            if typeOfOperation[1] != "BOOL":
                raise Exception(f"Operation with incompatible Types can't operate FOR with {typeOfOperation}")
            typeOfOperation = self.children[0].Evaluate(symbolTable)

class CondOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    def Evaluate(self,symbolTable):
        value = self.children[0].Evaluate(symbolTable)
        if value[1] != "BOOL":
            raise Exception(f"Operation with incompatible Types can't operate IF with {value[1]}")
        if len(self.children) == 3:
            if value[0]:
                self.children[1].Evaluate(symbolTable)
            else:
                self.children[2].Evaluate(symbolTable)
        else:
            if value[0]:
                self.children[1].Evaluate(symbolTable)

class AddTask(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, symbolTable):
        # Recupera a lista de tarefas a partir da SymbolTable
        todo_tasks = symbolTable.get("todo_tasks")[0]

        # Verifica se já existem 5 ou mais tarefas pendentes
        pendentes = sum(1 for t in todo_tasks if not t["feito"])
        if pendentes >= 5:
            print("Não posso adicionar mais tarefas. Você já está com muitas, coitado! Agora vai fazer elas!")
            return

        # Adiciona a nova tarefa
        todo_tasks.append({"nome": self.children[0], "feito": False})
        print(f'Tarefa adicionada: "{self.children[0]}"')


class ShowTasks(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, symbolTable):
        lista = symbolTable.get("todo_tasks")[0]
        print("Lista de tarefas:")
        for t in lista:
            status = "✅" if t["feito"] else "❌"
            print(f'- {t["nome"]} {status}')


class FinishTask(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, symbolTable):
        lista = symbolTable.get("todo_tasks")[0]
        nome = self.children[0]
        for t in lista:
            if t["nome"] == nome:
                t["feito"] = True
                print(f'Tarefa concluída: {nome}')
                return
        print(f"Tarefa não encontrada: {nome}")


class ClearAllTasks(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, symbolTable):
        symbolTable.get("todo_tasks")[0].clear()
        print("Lista de tarefas foi **resetada** com sucesso!")


class FeitoStatus(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, symbolTable):
        todo_tasks = symbolTable.get("todo_tasks")[0]
        pendentes = sum(1 for t in todo_tasks if not t["feito"])
        if pendentes > 0:
            print(f"Ainda faltam {pendentes} tarefas.")
        else:
            print("Sim, tudo pronto por agora!")



class ReadOp(Node):
    def __init__(self, value,children = None):
        super().__init__(value,children)
    def Evaluate(self,symbolTable):
        return (int(input()),"INT")

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class Return(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    def Evaluate(self, symbolTable):
        
        raise ReturnException(self.children.Evaluate(symbolTable))

class Block(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    def Evaluate(self,symbolTable):
        for statement in self.children:
            if statement.value == "BLOCK":
                local_table = SymbolTable(symbolTable)
                statement.Evaluate(local_table)
            elif statement.value == "RETURN":
                return statement.Evaluate(symbolTable)
            else:
                statement.Evaluate(symbolTable)
class FuncDec(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, symbolTable):
        func_name = self.children[0].value
        return_type = self.value
        symbolTable.create(func_name, (self, return_type, True))

class FuncCall(Node):
    def __init__(self, value, children):
        super().__init__(value, children)  # value = nome da função, children = lista de argumentos

    def Evaluate(self, symbol_table):
        name = self.value
        function = symbol_table.get(name)
        if symbol_table.get(name) == None:
            raise Exception(f"Function {name} not declared")
        
        func_node = function[0]
        return_type = function[1]

        if function[2] == False:
            raise Exception(f"{name} is not a function")

        expected_params = func_node.children[1:-1]  # Pula nome e bloco
        passed_args = self.children
        if len(expected_params) != len(passed_args):
            raise Exception(f"Wrong number of arguments for function {name} expected {len(expected_params)}, got {len(passed_args)}")
        local_symbol_table = SymbolTable(symbol_table)

        for i in range(len(expected_params)):
            param_type, param_identifier = expected_params[i]
            received_param = passed_args[i].Evaluate(symbol_table)
            if received_param[1] != dict_types[param_type]:
                raise Exception(f"Type mismatch for parameter {param_identifier.value}: "
                                f"expected {param_type}, got {received_param[1]}")
            local_symbol_table.create(param_identifier.value, (received_param[0], received_param[1]))
        
        try:
            result = func_node.children[-1].Evaluate(local_symbol_table)
        except ReturnException as ret:
            result = ret.value
            if dict_types[return_type] != result[1]:
                raise Exception(f"Type mismatch: {result[1]} and {return_type}")
            return result
class NoOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    def Evaluate(self,symbolTable):
        pass

class Token:
    def __init__(self, type:str,value):
        self.type = type
        self.value = value

class Tokenizer:
    def __init__(self, source: str):
        self.source = PrePro.filter(source)
        self.pos = 0
        self.current_char = None

    def selectNext(self):
        while self.pos < len(self.source) and self.source[self.pos] in [' ', '\t']:
            self.pos += 1

        if self.pos >= len(self.source):
            self.current_char = Token('EOF', None)
            return self.current_char

        c = self.source[self.pos]

        if c.isdigit():
            self.pos += 1
            while self.pos < len(self.source) and self.source[self.pos].isdigit():
                c += self.source[self.pos]
                self.pos += 1
            self.current_char = Token('NUMBER', c)
            return self.current_char

        elif c == '+':
            self.pos += 1
            self.current_char = Token('PLUS', c)
        elif c == '-':
            self.pos += 1
            self.current_char = Token('MINUS', c)
        elif c == '*':
            self.pos += 1
            self.current_char = Token('MULT', c)
        elif c == '/':
            self.pos += 1
            self.current_char = Token('DIV', c)
        elif c == '(':
            self.pos += 1
            self.current_char = Token('OPEN_PAR', c)
        elif c == ')':
            self.pos += 1
            self.current_char = Token('CLOSE_PAR', c)
        elif c == '>':
            self.pos += 1
            self.current_char = Token('BIGGER', c)
        elif c == '<':
            self.pos += 1
            self.current_char = Token('LOWER', c)
        elif c == '!':
            self.pos += 1
            self.current_char = Token('NOT', c)
        elif c == '&':
            self.pos += 1
            if self.source[self.pos] == '&':
                c += self.source[self.pos]
                self.pos += 1
                self.current_char = Token('AND', c)
            else:
                raise Exception('Expected another & for "&&" operator')
        elif c == '|':
            self.pos += 1
            if self.source[self.pos] == '|':
                c += self.source[self.pos]
                self.pos += 1
                self.current_char = Token('OR', c)
            else:
                raise Exception('Expected another | for "||" operator')
        elif c.isalpha() or c == '_':
            self.pos += 1
            while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
                c += self.source[self.pos]
                self.pos += 1
            if c == "Println":
                self.current_char = Token('PRINT', c)
            elif c == "Scan":
                self.current_char = Token('READ', c)
            elif c == "for":
                self.current_char = Token('WHILE', c)
            elif c == "if":
                self.current_char = Token('IF', c)
            elif c == "else":
                self.current_char = Token('ELSE', c)
            elif c == "var":
                self.current_char = Token('VARDEC', c)
            elif c in ["int", "bool", "string"]:
                self.current_char = Token("TYPE", c)
            elif c in ["true", "false"]:
                self.current_char = Token("BOOL", c)
            elif c == "func":
                self.current_char = Token("FUNCDEC", c)
            elif c == "return":
                self.current_char = Token("RETURN", c)
            # Adicionados para ToDoLang:
            elif c == "tarefa":
                self.current_char = Token("TAREFA", c)
            elif c == "mostrar":
                self.current_char = Token("MOSTRAR", c)
            elif c == "concluir":
                self.current_char = Token("CONCLUIR", c)
            elif c == "feito":
                self.current_char = Token("FEITO", c)
            elif c == "limpar_lista":
                self.current_char = Token("LIMPAR", c)
            elif c == "se":
                self.current_char = Token("IF", c)  # já reaproveita if
            elif c == "enquanto":
                self.current_char = Token("WHILE", c)  # já reaproveita while
            else:
                self.current_char = Token('IDENTIFIER', c)
        elif c == '=':
            self.pos += 1
            if self.source[self.pos] == '=':
                c += self.source[self.pos]
                self.pos += 1
                self.current_char = Token('EQUAL', c)
            else:
                self.current_char = Token('ASSIGN', c)
        elif c == '{':
            self.pos += 1
            self.current_char = Token('OPEN_BLOCK', c)
        elif c == '}':
            self.pos += 1
            self.current_char = Token('CLOSE_BLOCK', c)
        elif c == ',':
            self.pos += 1
            self.current_char = Token("COMMA", c)
        elif c == '\"':
            self.pos += 1
            c = ''
            while self.source[self.pos] != '"':
                c += self.source[self.pos]
                self.pos += 1
            self.pos += 1
            self.current_char = Token("STR", c)
        elif c == '\n':
            self.pos += 1
            self.current_char = Token('NEW_LINE', c)
        else:
            raise Exception(f"Invalid character {c}")

        return self.current_char


class Parser:
    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer
        self.tokenizer.selectNext()


    def parse_program(self):
        nodes = []
        while self.tokenizer.current_char.type != 'EOF':
            if self.tokenizer.current_char.type in [
                'TAREFA', 'MOSTRAR', 'CONCLUIR', 'STATUS', 'PENDENCIAS', 'LIMPAR', 'FEITO'
            ]:
                nodes.append(self.parse_todo_command())

            elif self.tokenizer.current_char.type in ['SE', 'ENQUANTO', 'IF', 'WHILE']:
                nodes.append(self.parse_statement())

            elif self.tokenizer.current_char.type == "FUNCDEC":
                nodes.append(self.parse_FuncDec())

            elif self.tokenizer.current_char.type == "VARDEC":
                nodes.append(self.parse_VarDec())

            elif self.tokenizer.current_char.type == "NEW_LINE":
                self.tokenizer.selectNext()

            else:
                raise Exception(f"Invalid Token in program {self.tokenizer.current_char.type}")
        
        return Block("BLOCK", nodes)



    def parse_todo_command(self):
        if self.tokenizer.current_char.type == 'TAREFA':
            self.tokenizer.selectNext()
            if self.tokenizer.current_char.type == 'STR':
                task = self.tokenizer.current_char.value
                self.tokenizer.selectNext()
                return AddTask("TAREFA", [task])
            else:
                raise Exception("Expected string after 'tarefa'")

        elif self.tokenizer.current_char.type == 'MOSTRAR':
            self.tokenizer.selectNext()
            return ShowTasks("MOSTRAR", [])

        elif self.tokenizer.current_char.type == 'CONCLUIR':
            self.tokenizer.selectNext()
            if self.tokenizer.current_char.type == 'STR':
                task = self.tokenizer.current_char.value
                self.tokenizer.selectNext()
                return FinishTask("CONCLUIR", [task])
            else:
                raise Exception("Expected string after 'concluir'")

        elif self.tokenizer.current_char.type == "STATUS":
            self.tokenizer.selectNext()
            return Print("PRINT", FuncCall("relatorio_pendencias", []))

        elif self.tokenizer.current_char.type == "PENDENCIAS":
            self.tokenizer.selectNext()
            return Print("PRINT", FuncCall("tarefas_pendentes", []))

        elif self.tokenizer.current_char.type == "LIMPAR":
            self.tokenizer.selectNext()
            return ClearAllTasks("LIMPAR", [])

        elif self.tokenizer.current_char.type == "FEITO":
            self.tokenizer.selectNext()
            return FeitoStatus("FEITO", [])

        else:
            raise Exception(f"Comando inválido: {self.tokenizer.current_char.type}")




    def parse_FuncDec(self):
        if self.tokenizer.current_char.type == "FUNCDEC":
            self.tokenizer.selectNext()
            if self.tokenizer.current_char.type == "IDENTIFIER":
                ident = Identifier(self.tokenizer.current_char.value)
                self.tokenizer.selectNext()
                if self.tokenizer.current_char.type == 'OPEN_PAR':
                    self.tokenizer.selectNext()
                    nodes = [ident] # O Primeiro nó é o nome da função e o ultimo nó é o bloco
                    while self.tokenizer.current_char.type != "CLOSE_PAR":
                        if self.tokenizer.current_char.type == "IDENTIFIER":
                            variable_ident = Identifier(self.tokenizer.current_char.value)
                            self.tokenizer.selectNext()
                            if self.tokenizer.current_char.type == "TYPE":
                                type_and_name = (self.tokenizer.current_char.value,variable_ident)
                                nodes.append(type_and_name)
                                self.tokenizer.selectNext()
                                if self.tokenizer.current_char.type == "COMMA":
                                    self.tokenizer.selectNext()
                                    if self.tokenizer.current_char.type == "CLOSE_PAR":
                                        raise Exception(f"Expected another variable after the COMMA")
                            else:
                                raise Exception(f"Expected a type declaration after the IDENTIFIER")
                        else:
                            raise Exception(f"This kind of token not expected in function params")
                    if self.tokenizer.current_char.type == "CLOSE_PAR":
                        self.tokenizer.selectNext()
                        tipo = None
                        if self.tokenizer.current_char.type == "TYPE":
                            tipo = self.tokenizer.current_char.value
                            self.tokenizer.selectNext()
                        nodes.append(self.parse_block())
                        node = FuncDec(tipo,nodes)
                        return node
                else:
                    raise Exception(f"Expected a Open Parentesis after the IDENTIFIER")
            else:
                raise Exception(f"Expected a IDENTIFIER after the FUNCDEC")
            
    def parse_VarDec(self):
        if self.tokenizer.current_char.type == "VARDEC":
            self.tokenizer.selectNext()
            if self.tokenizer.current_char.type == "IDENTIFIER":
                ident = Identifier(self.tokenizer.current_char.value)
                self.tokenizer.selectNext()
                if self.tokenizer.current_char.type == "TYPE":
                    declaration = [self.tokenizer.current_char.value]
                    self.tokenizer.selectNext()
                    if self.tokenizer.current_char.type == "ASSIGN":
                        self.tokenizer.selectNext()
                        declaration.insert(0,self.parse_bexpression())
                    node = VarDec(ident,declaration)
                    return node
                else:
                    raise Exception(f"TYPE expected after a IDENTIFIER in Variable Declaration but received:{self.tokenizer.current_char.type}")
            else:
                raise Exception(f"IDENTIFIER expected after a Variable Declaration but received:{self.tokenizer.current_char.type}")

    def parse_block(self):
        nodes = []
        if self.tokenizer.current_char.type == 'OPEN_BLOCK':
            self.tokenizer.selectNext()
            if self.tokenizer.current_char.type =='NEW_LINE':
                self.tokenizer.selectNext()
                while self.tokenizer.current_char.type != 'CLOSE_BLOCK':
                    nodes.append(self.parse_statement())
                if self.tokenizer.current_char.type == 'CLOSE_BLOCK':
                    self.tokenizer.selectNext()
                    return Block("BLOCK",nodes)
            else:
                raise Exception(f"Expected a CLOSE_BLOCK")
        else:
            raise Exception(f"Expected a Scope of block")
        
    def parse_statement(self):
        node = NoOp("NoOp", None)

        if self.tokenizer.current_char.type == 'IDENTIFIER':
            ident = Identifier(self.tokenizer.current_char.value)
            self.tokenizer.selectNext()
            if self.tokenizer.current_char.type == 'ASSIGN':
                self.tokenizer.selectNext()
                node = Assigment(ident, self.parse_bexpression())
            elif self.tokenizer.current_char.type == 'OPEN_PAR':
                self.tokenizer.selectNext()
                nodes = []
                while self.tokenizer.current_char.type != 'CLOSE_PAR':
                    nodes.append(self.parse_bexpression())
                    if self.tokenizer.current_char.type == 'COMMA':
                        self.tokenizer.selectNext()
                        if self.tokenizer.current_char.type == 'CLOSE_PAR':
                            raise Exception(f"Expected another variable after the COMMA")
                if self.tokenizer.current_char.type == 'CLOSE_PAR':
                    self.tokenizer.selectNext()
                    node = FuncCall(ident.value, nodes)
            else:
                raise Exception(f"Invalid Token after identifier {self.tokenizer.current_char.type}")

        elif self.tokenizer.current_char.type == 'PRINT':
            self.tokenizer.selectNext()
            if self.tokenizer.current_char.type == 'OPEN_PAR':
                self.tokenizer.selectNext()
                expr = self.parse_bexpression()
                if self.tokenizer.current_char.type == 'CLOSE_PAR':
                    self.tokenizer.selectNext()
                    node = Print("PRINT", expr)
                else:
                    raise Exception("Expected closing parenthesis in print")

        elif self.tokenizer.current_char.type == 'VARDEC':
            node = self.parse_VarDec()

        elif self.tokenizer.current_char.type == 'WHILE':
            self.tokenizer.selectNext()
            cond = self.parse_bexpression()
            bloco = self.parse_block()
            node = While("WHILE", [cond, bloco])

        elif self.tokenizer.current_char.type == 'IF':
            self.tokenizer.selectNext()
            cond = self.parse_bexpression()
            bloco_then = self.parse_block()
            children = [cond, bloco_then]
            if self.tokenizer.current_char.type == 'ELSE':
                self.tokenizer.selectNext()
                bloco_else = self.parse_block()
                children.append(bloco_else)
            node = CondOp("COND", children)

        elif self.tokenizer.current_char.type == 'RETURN':
            self.tokenizer.selectNext()
            expr = self.parse_bexpression()
            node = Return("RETURN", expr)

        elif self.tokenizer.current_char.type == 'OPEN_BLOCK':
            node = self.parse_block()

        elif self.tokenizer.current_char.type in ['TAREFA', 'MOSTRAR', 'CONCLUIR']:
            node = self.parse_todo_command()

        else:
            raise Exception(f"Invalid Token in statement: {self.tokenizer.current_char.type}")

        if self.tokenizer.current_char.type == "NEW_LINE":
            self.tokenizer.selectNext()
        return node


        
    
    def parse_bexpression(self):
        node = self.parse_bterm()
        while self.tokenizer.current_char.type in ['OR']:
            self.tokenizer.selectNext()
            node = BinOp('||',[node,self.parse_bterm()])
        return node

    def parse_bterm(self):
        node = self.parse_relexpression()
        while self.tokenizer.current_char.type in ['AND']:
            self.tokenizer.selectNext()
            node = BinOp('&&',[node,self.parse_relexpression()])
        return node

    def parse_relexpression(self):
        node = self.parse_expression()
        while self.tokenizer.current_char.type in ['EQUAL','BIGGER','LOWER']:
            if self.tokenizer.current_char.type == 'EQUAL':
                self.tokenizer.selectNext()
                node = BinOp('==',[node,self.parse_expression()])
            elif self.tokenizer.current_char.type == 'BIGGER':
                self.tokenizer.selectNext()
                node = BinOp('>',[node,self.parse_expression()])
            else:
                self.tokenizer.selectNext()
                node = BinOp('<',[node,self.parse_expression()])
        return node
    
    def parse_expression(self):
        node = self.parse_term()
        while self.tokenizer.current_char.type in ['PLUS', 'MINUS']:
            if self.tokenizer.current_char.type == 'PLUS':
                self.tokenizer.selectNext()
                node = BinOp('+', [node, self.parse_term()])
            else:
                self.tokenizer.selectNext()
                node = BinOp('-', [node, self.parse_term()])
        return node
            
    def parse_term(self):
            node = self.parse_factor()
            while self.tokenizer.current_char.type in ['MULT', 'DIV']:
                if self.tokenizer.current_char.type == 'MULT':
                    self.tokenizer.selectNext()
                    node = BinOp('*', [node, self.parse_factor()])
                else:
                    self.tokenizer.selectNext()
                    node = BinOp('/', [node, self.parse_factor()])
            return node

    def parse_factor(self):
        if self.tokenizer.current_char.type == 'NUMBER':
            node = IntVal(self.tokenizer.current_char.value, [])
            self.tokenizer.selectNext()
            return node
        elif self.tokenizer.current_char.type == "IDENTIFIER":
            node = Identifier(self.tokenizer.current_char.value)
            self.tokenizer.selectNext()
            if self.tokenizer.current_char.type == "OPEN_PAR":
                self.tokenizer.selectNext()
                nodes = []
                while self.tokenizer.current_char.type != "CLOSE_PAR":
                    nodes.append(self.parse_bexpression())
                    if self.tokenizer.current_char.type == "COMMA":
                        self.tokenizer.selectNext()
                        if self.tokenizer.current_char.type == "CLOSE_PAR":
                            raise Exception(f"Expected another variable after the COMMA")
                if self.tokenizer.current_char.type == "CLOSE_PAR":
                    self.tokenizer.selectNext()
                    node = FuncCall(node.value,nodes)
            return node
        elif self.tokenizer.current_char.type == "STR":
            node = StrVal(self.tokenizer.current_char.value, [])
            self.tokenizer.selectNext()
            return node
        elif self.tokenizer.current_char.type == "BOOL":
            node = BoolVal(self.tokenizer.current_char.value, [])
            self.tokenizer.selectNext()
            return node
        elif self.tokenizer.current_char.type == "READ":
            self.tokenizer.selectNext()
            if self.tokenizer.current_char.type == "OPEN_PAR":
                self.tokenizer.selectNext()
                if self.tokenizer.current_char.type == "CLOSE_PAR":
                    self.tokenizer.selectNext()
                    return ReadOp("READ")
            return node
        elif self.tokenizer.current_char.type == "PLUS":
            self.tokenizer.selectNext()
            return UnOp('+', [self.parse_factor()])
        elif self.tokenizer.current_char.type == "MINUS":
            self.tokenizer.selectNext()
            return UnOp('-', [self.parse_factor()])
        elif self.tokenizer.current_char.type == "NOT":
            self.tokenizer.selectNext()
            return UnOp('!', [self.parse_factor()])
        elif self.tokenizer.current_char.type == "OPEN_PAR":
            self.tokenizer.selectNext()
            node = self.parse_bexpression()
            if self.tokenizer.current_char.type == "CLOSE_PAR":
                self.tokenizer.selectNext()
                return node
            else:
                raise Exception(f"Faltando o Close Par {self.tokenizer.current_char.type}")
        else:
            raise Exception('Error in parsefactor')
    

    def run(code):
        tokenizer = Tokenizer(code)
        parser = Parser(tokenizer)
        result = parser.parse_program()
        if parser.tokenizer.current_char.type != 'EOF':
            raise Exception(f"EOF esperado {parser.tokenizer.current_char.type}")
        return result

def main():
    file = sys.argv[1]
    if not file.endswith('.todo'):
        raise Exception("O arquivo precisa ter extensão .todo")

    with open(file, 'r', encoding='utf-8') as f:
        source = f.read()

    result = Parser.run(source)
    symbolTable = SymbolTable()
    symbolTable.create("todo_tasks", ([], "list"))
    result.Evaluate(symbolTable)
    
if __name__ == '__main__':
    main()
