# Компилятор языка "О"
import pars
import scan
import text

print('Компилятор языка "MODULA-2"')

def Init():
    text.Reset()
    pars.TestScan()

def Done():
    pass

Init()
#pars.TestText()
#pars.TestScan()
#pars.Compile()
print()
print("Компиляция завершена")
Done()