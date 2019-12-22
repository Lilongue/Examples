"""
Классы для отображения и хранения информации о игровом поле
"""

class SudoLine(object):
    """
    Класс для хранения столбцов/строк/квадратов
    """
    full_values_set = "123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    value_set = None
    def __init__(self, dimention = 3, overwrite = True):
        self.__dim = dimention
        if dimention < 2 or dimention > 5:
            self.__dim = 3
        self.value_set = set(self.full_values_set[:self.__dim*self.__dim])
        self.__current_set = set(list(self.value_set))
        self.__line = [None for i in range(self.__dim* self.__dim)]
        self.overwrite = overwrite
          
    @property
    def dim(self):
        """
        Свойство, содержащее число измерений нашего судоку
        """
        return self.__dim

    @property
    def values(self):
        """
        Возвращает список с заполнеными значениями
        """
        return self.__line

    @property
    def current_set(self):
        """
        Возвращает текущие допустимые значения символов для вставки (неотгаданные символы) Type = set
        """
        return self.__current_set

    def can_insert(self, symbol, position):
        """Проверяет на возможность вставки символа в указанную позицию
        
        Arguments:
            symbol {String} -- [Вставляемый символ]
            position {Integer} -- [Позиция для вставки. Нумерация с единицы!]
        
        Returns:
            [Integer] -- [0 - символ не относится к числу допустимых; 1 - символ допустим, но позиция занята;
            2 - символ допустим и позиция для вставки свободна]
        """
        if symbol not in self.__current_set:
            return 0
        if self.__line[position-1] is not None:
            return 1
        return 2

        
    def insert(self, symbol, position):
        """
        Метод вставляет символ в указанную позицию, если это допустимо
        
        Arguments:
            symbol {[string]} -- [символ для вставки]
            position {[int]} -- [позиция для вставки (номерация с единицы)]
        
        Returns:
            [type] -- [description]
        """
        state = self.can_insert(symbol,position)
        if not state:
            return (False, state, "Символ не допустим")
        if state == 1 and not self.overwrite:
            return (False, state, "Позиция уже занята и автозамена отключена")
        if state == 2:
            self.values[position-1] = symbol
            self.__current_set.remove(symbol)
            return (True, state, "Символ вставлен в пустую позицию")
        if state == 1 and self.overwrite:
            self.__current_set.add(self.values[position-1])
            self.values[position-1] = symbol
            self.__current_set.remove(symbol)
            return (False, state, "Символ заменен")
        
    def delete(self, position):
        """
        Удаление символа из указанной позиции        
        Arguments:
            position {[integer]} -- [Номер позиции символа. Нумерация с единицы!]
        
        Returns:
            [bool] -- [True - удаление было совершено; False - ничего удалено не было]
        """
        if position > len(self.values) or position < 1:
            return False
        if self.values[position-1] is not None:
            self.__current_set.add(self.values[position-1])    
            self.values[position-1] = None
            return True
        return False

    def to_str(self, wide = False):
        """
        преобразует значения в строку для вывода поля игры в консоль        
        Keyword Arguments:
            wide {bool} -- [Делает поле шире в случае True] (default: {False})
        
        Returns:
            {string} -- [Строка для печати поля]
        """
        if wide:
            sep = " | "
        else:
            sep = "|"
        out = sep
        for i in self.values:
            if i is None:
                out += " "
            else:
                out += i
            out += sep
        return out

    def __str__(self):
        """
        Вывод функции print()
        """
        return ("Размерность: "+ str(self.__dim) + "\n" + "Набор символов: " + str(self.value_set) + "\n")

class Board(object):

    h_head = list("abcdefghijklmnopqrstuvwxyz")
    v_head = [i+1 for i in range(25)]
    sep_line = "+-"

    def __init__(self, dimention = 3, overwrite = True):
        self.__dim = dimention
        if dimention < 2 or dimention > 5:
            self.__dim = 3
        self.overwrite = overwrite
        self.main_lines = [SudoLine(dimention , overwrite)]*(self.__dim*self.__dim)
        self.v_lines = [SudoLine(self.__dim, self.overwrite) for i in range(self.__dim*self.__dim)]
        self.sq_lines = [SudoLine(self.__dim, self.overwrite) for i in range(self.__dim*self.__dim)]

    def index_from_mark(h, v):
        out = [0,0]
        if type(h) == type(1):
            out[0] = h
        elif type(h) == type("str"):
            try:
                out[0] = int(h)
        if type(v) == type("str"):
            for i,l 




if __name__ == "__main__":
    import doctest
    doctest.testmod()
    s3 = SudoLine(3)
    s2 = SudoLine(2)
    s4 = SudoLine(4)
    s5 = SudoLine(5)
    s6 = SudoLine(6)
    s0 = SudoLine(0)
    print(s2)
    print(s3)
    print(s4)
    print(s5)
    print(s6)
    print(s0)
