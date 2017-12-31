# ShenMeCC

a simple and stupid compiler collection(just now for PL0, support for other languages may be added someday)

## __directory__

- Lexer(#lexer)
    - [PL0](#lexerpl0)
- Parser(#parser)
    - [PL0](#parserpl0)
- DataStruct(#datastruct)
    - [Tree](#datastructtree.py)
    - [SyntaxTree.py](#datastructsyntaxtree.py)
- VM

### Lexer

define `AbstractLexer`, which has input(), hasnext(), forward(), backward().

### parser

define `AbstractParser`, which has call(), parse().

### Lexer/PL0

define some class that used in lexer analysis for PL0.

in SimpleLexer.py define a subclass of `AbstractLexer` named SimpleLexer and `Statement` to store source code. add function `next_character_safe` in `SimpleLexer` to prevent exception when contining read whlie EOF reached. add function `get_int` make is simple for float detection(though it is not defined in PL0). use dict to make token analysis simple.

### Parser/PL0

### DataStruct/Tree.py

### DataStruct/SyntaxTree.py