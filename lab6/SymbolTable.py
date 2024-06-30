class SymbolTableDict:
    def __init__(self):
        self.symbol_tables = {}

    def add_table(self, table_name):
        if table_name in self.symbol_tables:
            raise RedefinitionError(table_name, 'table_dict')
        self.symbol_tables[table_name] = SymbolTable(table_name)

    def get_table(self, table_name):
        if table_name not in self.symbol_tables:
            raise NotFoundError(table_name, 'table_dict')
        return self.symbol_tables[table_name]

    def __str__(self):
        return "\n".join(f"{name}@table:"+ '\n{' + f"{str(table)}" + '\n}' for name, table in self.symbol_tables.items())

class SymbolTable:
    def __init__(self, table_name):
        self.table_name = table_name
        self.symbol_table = {'name':table_name, 'outer': None, 'width': None, 'rtype': None, 'argc': None, 'arglist': None, 'code':f'{table_name}@code'}

    def add_symbol(self, name, type, **kwargs):
        if name in self.symbol_table:
            raise RedefinitionError(name, 'symbol_table')
        self.symbol_table[name] = {'type': type, **kwargs}

    def set_attribute(self, name, attribute, value):
        if name not in self.symbol_table:
            raise NotFoundError(name, 'symbol_table')
        self.symbol_table[name][attribute] = value

    def get_symbol(self, name):
        if name not in self.symbol_table:
            raise NotFoundError(name, 'table_dict')
        return self.symbol_table.get(name)
    
    def __str__(self):
        symbol_info = "\n".join(f"{name}: {info}" for name, info in self.symbol_table.items())
        return f"\n{symbol_info}"
    
class RedefinitionError(Exception):
    def __init__(self, name, type):
        self.name = name
        self.type = type
        super().__init__(f"'{name}' has already been defined in {type}")

class NotFoundError(Exception):
    def __init__(self, name, type):
        self.name = name
        super().__init__(f"'{name}' is not found in {type}")
    
if __name__ == '__main__':
    # 创建 SymbolTableDict 实例
    symbol_dict = SymbolTableDict()

    # 添加新表
    symbol_dict.add_table('main')

    # 向 'main' 表中添加符号
    symbol_dict.get_table('main').add_symbol('int', 'x', value=5)
    symbol_dict.get_table('main').add_symbol('float', 'y', value=3.14)

    # 打印符号表
    print(symbol_dict)
