# ShenMeCC

a simple and stupid compiler collection(just now for PL0, support for other languages may be added someday)

## __Content__

- [Introduction](#introduction)
- [Features](#features)
- [File Directory](#file-directory)

## __Introduction__

this is a compiler collection(though it just support PL0). i am trying to make it extendable by defining dozen of abstract class.

## __Features__

1. Chinese identifier is supported
2. error report is detailed in lexer analysis, sytax analysis
3. can get parse tree and syntax tree
4. debug or verbose mode for VM is supported. support for single step excute and displaying stack, instruct, register.

## __File Directory__

- [Lexer](#lexer)
    - [PL0](#lexerpl0)
- [Parser](#parser)
    - [PL0](#parserpl0)
- [DataStruct](#datastruct)
    - [Tree](#datastructtreepy)
    - [SyntaxTree.py](#datastructsyntaxtreepy)
- [VM](#vm)
    - [PCode](#vmpcode)
        - [PCodeGen.py](#vmpcodepcodegenpy)
        - [PCodeVM.py](#vmpcodepcodevmpy)

### Lexer

define `AbstractLexer`, which has input(), hasnext(), forward(), backward().

### parser

define `AbstractParser`, which has call(), parse().

### DataStruct

define some datastruct that used commonly in each period of compiler, such as [`SyntaxTree`](#datastructsyntaxtreepy) for syntax analysis.

### VM

define `AbstractGen` a interface for semantic analyzer and `AbstractVM` a interface for virtual machine.

### Lexer/PL0

define some class that used in lexer analyzer for PL0.

in SimpleLexer.py define a subclass of `AbstractLexer` named SimpleLexer and `Statement` to store source code. add function `next_character_safe` in `SimpleLexer` to prevent exception when contining read whlie EOF reached. add function `get_int` make is simple for float detection(though it is not defined in PL0). use dict to make token analysis simple.

### Parser/PL0

in RecursiveParser.py define a subclass of `AbstractParser` named RecursiveParser, which is a typical recursive down parser with function named in Chinese(little bit strange). instacne of this class is callable with input of source code(type str), output analysis tree and syntax tree.

### DataStruct/Tree.py

define a tree type struct with `gencode()` and `print()`. `gencode()` is designed to support semantic analysis. `print()` is designed for print.

### DataStruct/SyntaxTree.py

in this file, define series of class with semantic meanings, such as `VariableDeclaration`, `AssignExpression`. each class defined in this file should be subclass of `TreeNode`.

interface gencode is implement in each class which accept two arguments: symbol table and code, returning nothing but may raise SemanticException.

### VM/PCode/PCodeGen.py

in this file, define `SymbolTable` and  `PCodeGener` which is a subclass of `AbstractGen`.

`SymbolTable` uses a stack based block symbol table.

`PCodeGener` is callable with AST as input and P-Code as output. it is just create a instance of `SymbolTable` and a list as the container of p-Code at beginning, then call AST's `gencode` function to generate P-Code.

### VM/PCode/PCodeVM.py

in this file, define `PCodeVM` which is a subclass of `AbstractVM`.

constructor of `PCodeVM` accept some keyword argument, which indicate the VM runs in debug mode or verbose mode

instance of `PCodeVM` is callable, accepting a list of P-Code and excute it. using dict and higher-corder function to make it simple to implement.