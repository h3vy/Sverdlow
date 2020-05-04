# Таблица имен

_table = []

def openScope():
    _table.append({})

def closeScope():
    _table.pop()

def add(item):
    last = _table[-1]
    last[item.key] = item

def new(item):
    pass



