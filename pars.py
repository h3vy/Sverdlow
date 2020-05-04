# Синтаксический анализатор

from text import *
from scan import *
from table import *


def TestText():
    while ch() != chEOT:
        nextCh()


def TestScan():
    nextCh()
    nextLex()
    n = 0
    LexDict = dict()
    while lex() != Lex.EOT:
        n += 1
        lx = lex()
        if lx in LexDict:
            LexDict[lx] += 1
        else:
            LexDict[lx] = 1
        nextLex()
    print()
    print("Число лексем", n)
    for lx in LexDict:
        print(lx, LexDict[lx], LexDict[lx]/n*100,'%')


def skip(L):
    if lex() == L:
        nextLex()
    else:
        expect(lexName(L))


# Импорт =
#    IMPORT Имя {"," Имя} ";".
def Import():
    skip(Lex.IMPORT)
    skip(Lex.NAME)
    while lex() == Lex.COMMA:
        nextLex()
        skip(Lex.NAME)
    skip(Lex.SEMI)


# КонстВыраж = ["+" | "-"] (Число | Имя).
def ConstExpr():
    if lex() in {Lex.PLUS, Lex.MINUS}:
        nextLex()
    if lex() in {Lex.NUM, Lex.NAME}:
        nextLex()
    else:
        expect("число или имя")


# ОбъявлКонст = Имя "=" КонстВыраж.
def ConstDecl():
    skip(Lex.NAME)
    skip(Lex.EQ)
    ConstExpr()


def Type():
    skip(Lex.NAME)


# ОбъявлПерем = Имя {"," Имя} ":" Тип.
def VarDecl():
    skip(Lex.NAME)
    while lex() == Lex.COMMA:
        nextLex()
        skip(Lex.NAME)
    skip(Lex.COLON)
    Type()


# ПослОбъявл =
#    {CONST
#       {ОбъявлКонст ";"}
#    |VAR
#       {ОбъявлПерем ";"} }.
def DeclSeq():
    while lex() in {Lex.CONST, Lex.VAR}:
        if lex() == Lex.CONST:
            nextLex()
            while lex() == Lex.NAME:
                ConstDecl()
                skip(Lex.SEMI)
        else:  # VAR
            nextLex()
            while lex() == Lex.NAME:
                VarDecl()
                skip(Lex.SEMI)


# ПростоеВыраж = ["+"|"-"] Слагаемое {ОперСлож Слагаемое}.
def SimpleExpression():
    if lex() in {Lex.PLUS, Lex.MINUS}:
        nextLex()
    Term()
    while lex() in {Lex.PLUS, Lex.MINUS}:
        nextLex()
        Term()


# Слагаемое = Множитель {ОперУмн Множитель}.
def Term():
    Factor()
    while lex() in {Lex.MULT, Lex.DIV, Lex.MOD}:
        nextLex()
        Factor()


# Множитель =
#    Имя ["(" Выраж ")"]
#    | Число
#    | "(" Выраж ")".
def Factor():
    if lex() == Lex.NAME:
        nextLex()
        if lex() == Lex.LPAR:
            nextLex()
            Expression()
            skip(Lex.RPAR)
    elif lex() == Lex.NUM:
        nextLex()
    elif lex() == Lex.LPAR:
        nextLex()
        Expression()
        skip(Lex.RPAR)
    else:
        expect("имя, число или '('")


# Выраж = ПростоеВыраж [Отношение ПростоеВыраж].
def Expression():
    SimpleExpression()
    if lex() in {Lex.EQ, Lex.NE, Lex.GT, Lex.GE, Lex.LT, Lex.LE}:
        nextLex()
        SimpleExpression()


def Parameter():
    Expression()


# Переменная ":=" Выраж
def AssStatement():
    # Переменная уже пропущена
    skip(Lex.ASS)
    Expression()


# [Имя "."] Имя ["(" [Параметр {"," Параметр}] ")"]
def CallStatement():
    # Имя уже прочитано
    if lex() == Lex.DOT:
        nextLex()
        skip(Lex.NAME)

    if lex() == Lex.LPAR:
        nextLex()
        if lex() != Lex.RPAR:
            Parameter()
            while lex() == Lex.COMMA:
                nextLex()
                Parameter()
        skip(Lex.RPAR)


# Переменная ":=" Выраж
# |[Имя "."] Имя ["(" [Параметр {"," Параметр}] ")"]
def AssOrCall():
    skip(Lex.NAME)
    if lex() == Lex.ASS:
        AssStatement()
    else:
        CallStatement()

#    IF Выраж THEN
#       ПослОператоров
#    {ELSIF Выраж THEN
#       ПослОператоров}
#    [ELSE
#       ПослОператоров]
#     END
def IfStatement():
    skip(Lex.IF)
    Expression()
    skip(Lex.THEN)
    StatSeq()
    while lex() == Lex.ELSIF:
        nextLex()
        Expression()
        skip(Lex.THEN)
        StatSeq()
    if lex() == Lex.ELSE:
        nextLex()
        StatSeq()
    skip(Lex.END)


# WHILE Выраж DO
#       ПослОператоров
# END
def WhileStatement():
    skip(Lex.WHILE)
    Expression()
    skip(Lex.DO)
    StatSeq()
    skip(Lex.END)



# Оператор = [
#    Переменная ":=" Выраж
#    |[Имя "."] Имя ["(" [Параметр {"," Параметр}] ")"]
#    |IF Выраж THEN
#       ПослОператоров
#    {ELSIF Выраж THEN
#       ПослОператоров}
#    [ELSE
#       ПослОператоров]
#     END
#    |WHILE Выраж DO
#       ПослОператоров
#     END
# ].
def Statement():
    if lex() == Lex.NAME:
        AssOrCall()
    elif lex() == Lex.IF:
        IfStatement()
    elif lex() == Lex.WHILE:
        WhileStatement()


# ПослОператоров =
#    Оператор {";"
#    Оператор }.
def StatSeq():
    Statement()
    while lex() == Lex.SEMI:
        nextLex()
        Statement()


# Модуль =
#    MODULE Имя ";"
#    [Импорт]
#    ПослОбъявл
#    [BEGIN
#       ПослОператоров]
# END Имя ".".
def Module():
    skip(Lex.MODULE)
    skip(Lex.NAME)
    skip(Lex.SEMI)
    if lex() == Lex.IMPORT:
        Import()
    DeclSeq()
    if lex() == Lex.BEGIN:
        nextLex()
        StatSeq()
    skip(Lex.END)
    skip(Lex.NAME)
    skip(Lex.DOT)


def Compile():
    nextCh()
    nextLex()
    openScope()

    openScope()
    Module()
    closeScope()
    closeScope()
