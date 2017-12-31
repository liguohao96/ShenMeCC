# ShenMeCC

a simple and stupid compiler collection(just now for PL0, support for other languages may be added someday)

## __directory__

- Lexer
    - [PL0](#lexerpl0)
- Parser
- VM

### Lexer/PL0

define a subclass of `AbstractLexer` named SimpleLexer and `Statement` to store source code.

add `next_character_safe` in `SimpleLexer`, prevent exception when contining read whlie EOF reached.

